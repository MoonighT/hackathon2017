import json
import os

import classification_manager
from const import DirectoryType, ImageCategory, Occasion, SCENARIO_DETAILS
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
						"title": "View",
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
		all_files = get_all_wardrobe(user_id)

		for is_top, file in all_files:
			file_dir = misc.get_file_directory(user_id, DirectoryType.DIR_TOP if is_top else DirectoryType.DIR_BOTTOM, file)
			probability = classification_manager.get_image_occasion_probability("male", file_dir, Occasion.FORMAL)


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

	top_files = misc.get_files_in_directory(user_id, DirectoryType.DIR_TOP)
	bottom_files = misc.get_files_in_directory(user_id, DirectoryType.DIR_BOTTOM)
	all_files = [(True, file) for file in top_files]
	all_files += [(False, file) for file in bottom_files]

	will_end = len(all_files) <= offset + 10

	range = xrange(offset, len(all_files)) if will_end else xrange(offset, offset + 9)
	elements = [_compose_cloth_entry(all_files[i][0], all_files[i][1]) for i in range]
	if not will_end:
		# append more option
		elements.append({

		})
	print elements
	print json.dumps(elements)

	bot_client.send_generic_message(user_id, elements)
