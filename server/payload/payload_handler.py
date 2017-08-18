import json
import os

import copy
from random import shuffle
from const import ImageCategory, DirectoryType, SCENARIO_DETAILS, Occasion
import classification_manager
import recommend_manager
from payload import Payload
from utils import files, misc
from utils.misc import generate_payload


def process_payload(bot_client, user_id, payload_serialized):
	payload = decode_payload(payload_serialized)
	if not payload:
		return None
	return handle_payload(bot_client, user_id, payload)


def decode_payload(payload_serialized):
	payload_dict = json.loads(payload_serialized)
	if "type" in payload_dict and "id" in payload_dict and "data" in payload_dict:
		return Payload(payload_dict)
	return None


def handle_payload(bot_client, user_id, payload):
	if payload.type == "image_recog":
		file_name = payload.id
		src_dir = misc.get_file_directory(user_id, DirectoryType.DIR_TEMP, file_name)
		if payload.data == ImageCategory.CAT_NONE:
			# remove image from temp
			os.remove(src_dir)
		else:
			# move image to destination folder
			dest_dir_type = DirectoryType.DIR_TOP if payload.data == ImageCategory.CAT_TOP else DirectoryType.DIR_BOTTOM
			dest_dir = misc.get_file_directory(user_id, dest_dir_type, file_name)
			os.rename(src_dir, dest_dir)
		bot_client.send_text_message(user_id, "OK")
	elif payload.type == "view_wardrobe":
		list_wardrobe(bot_client, user_id, 0)
	elif payload.type == "see_suggestion":
		bot_client.send_text_message(user_id, "Please select from the below occasions:")
		elements = []
		for key, value in SCENARIO_DETAILS.iteritems():
			element = {
				"buttons": [
					{
						"type": "postback",
						"title": "View %s" % value["title"],
						"payload": generate_payload("view_suggestions", "", key)
					}
				]
			}
			for k, v in value.iteritems():
				element[k] = v
			elements.append(element)
		bot_client.send_generic_message(user_id, elements)
	elif payload.type == "view_suggestions":
		occasion = payload.data
		show_suggestions_for_occasion(bot_client, user_id, occasion)
	elif payload.type == "remove_file":
		file_name = payload.data
		remove_clothes(bot_client, user_id, file_name)


def show_suggestions_for_occasion(bot_client, user_id, occasion):
	def _show_wardrobe_suggestion(suggestion):
		return {
			"title": "Top from your wardrobe",
			"subtitle": "You can select this as your top from your wardrobe",
			"image_url": files.get_file_url(suggestion["path"]),
		}

	def _show_external_suggestion(suggestion):
		return {
			"title": "Suggested new item to purchase",
			"subtitle": "It seems like you are running out of suitable options for this occasion. Perhaps it is time to consider getting a few new pieces to your wardrobe?",
			"image_url": suggestion["path"],
			"default_action": {
				"type": "web_url",
				"url": suggestion["reference"],
				"messenger_extensions": False,
				"webview_height_ratio": "tall",
			},
		}

	elements = []
	suggestions = get_suggestions_for_occasion(user_id, occasion)
	print json.dumps(suggestions)
	for suggestion in suggestions:
		elements.append(_show_wardrobe_suggestion(suggestion) if suggestion["type"] == "wardrobe" else _show_external_suggestion(suggestion))

	bot_client.send_generic_message(user_id, elements)
	bot_client.send_quick_replies(user_id, "What do you think of the suggestions?", [
		{
			"content_type": "text",
			"title": "Ya I like them",
			"payload": generate_payload("satisfaction", "", True)
		},
		{
			"content_type": "text",
			"title": "Hmm can be better?",
			"payload": generate_payload("satisfaction", "", False)
		}
	])


def normalize_suggestion_list(suggestions, occasion, image_cat):
	shuffle(suggestions)

	if len(suggestions) >= 2:
		return suggestions[0:2]

	# get from recommend
	recom_top = recommend_manager.get_image_recommend(occasion, "top" if image_cat == ImageCategory.CAT_TOP else "bottom")
	recom_top = recom_top[0:2 - len(suggestions)]
	for recom in recom_top:
		suggestions.append({
			"type": "external",
			"path": recom["image"],
			"reference": recom["purchase"],
			"category": image_cat,
		})
	return suggestions


def get_suggestions_for_occasion(user_id, occasion):
	all_files = get_all_wardrobe(user_id)
	top_suggest = []
	bottom_suggest = []
	for is_top, file in all_files:
		file_dir = misc.get_file_directory(user_id, DirectoryType.DIR_TOP if is_top else DirectoryType.DIR_BOTTOM, file)
		probability = classification_manager.get_image_occasion_probability(file_dir, 'male', occasion)
		if probability > 0.6:
			suggestion_list = top_suggest if is_top else bottom_suggest
			suggestion_list.append({
				"type": "wardrobe",
				"path": file,
				"category": ImageCategory.CAT_TOP if is_top else ImageCategory.CAT_BOTTOM
			})

	top_suggest = normalize_suggestion_list(top_suggest, occasion, ImageCategory.CAT_TOP)
	bottom_suggest = normalize_suggestion_list(bottom_suggest, occasion, ImageCategory.CAT_BOTTOM)
	return top_suggest + bottom_suggest


def remove_clothes(bot_client, user_id, file_name):
	top_file_dir = misc.get_file_directory(user_id, DirectoryType.DIR_TOP, file_name)
	bottom_file_dir = misc.get_file_directory(user_id, DirectoryType.DIR_BOTTOM, file_name)
	print top_file_dir
	print bottom_file_dir
	if os.path.exists(top_file_dir):
		print "top file exist"
		os.remove(top_file_dir)
	elif os.path.exists(bottom_file_dir):
		print "bottom file exist"
		os.remove(bottom_file_dir)
	bot_client.send_text_message(user_id, "OK, I will take care of that!")


def get_all_wardrobe(user_id):
	top_files = misc.get_files_in_directory(user_id, DirectoryType.DIR_TOP)
	bottom_files = misc.get_files_in_directory(user_id, DirectoryType.DIR_BOTTOM)
	all_files = [(True, file) for file in top_files]
	all_files += [(False, file) for file in bottom_files]
	return all_files


def list_wardrobe(bot_client, user_id, offset):
	def _compose_cloth_entry(is_top, file):
		return {
			"title": "Top" if is_top else "Legwear",
			"image_url": files.get_file_url(file),
			"buttons": [
				{
					"type": "postback",
					"title": "Remove",
					"payload": generate_payload("remove_file", "", file)
				}
			]
		}

	all_files = get_all_wardrobe(user_id)

	if not all_files:
		bot_client.send_text_message(user_id, "Hmm you don't have anything in your wardrobe. Try add some now?")
		return

	will_end = len(all_files) <= offset + 10

	range = xrange(offset, len(all_files)) if will_end else xrange(offset, offset + 9)
	elements = [_compose_cloth_entry(all_files[i][0], all_files[i][1]) for i in range]
	if not will_end:
		# append more option
		elements.append({
			"title": "You have a great collection :D",
			# todo: replace with better view more
			"image_url": "http://www.allschools.org/catalog/view/theme/metronicnew/eadmission/newtheme/view1.png",
			"buttons": [
				{
					"type": "postback",
					"title": "View More",
					"payload": generate_payload("view_wardrobe", "", offset + 9)
				}
			]
		})
	bot_client.send_generic_message(user_id, elements)
