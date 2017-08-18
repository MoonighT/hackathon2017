import json
import operator
import os

from flask import Flask
from flask import request
from pymessenger import Bot

import classification_manager
from const import CAT_TO_NAME, ImageCategory, DirectoryType
from utils import misc, parser
from utils.misc import download_file_from_url, get_file_directory

PAGE_ID = os.getenv("page_id")
if not PAGE_ID:
	raise Exception("page id is missing")

PAGE_TOKEN = os.getenv("page_token")
if not PAGE_TOKEN:
	raise Exception("page token is missing")

bot_client = Bot(PAGE_TOKEN)
app = Flask(__name__)

CATEGORY_PROBABILITY_THRESHOLD = 0.6


@app.route("/webhook", methods=['GET', 'POST'])
def process_fb_webhook():
	print "==========================="
	print "receive data"
	print request.data
	print "==========================="

	if request.method == 'GET':
		hub_challenge = request.args.get('hub.challenge')
		return hub_challenge
	else:
		data = json.loads(request.data)
		messages = data["entry"][0]["messaging"]
		for message in messages:
			process_message(message)
		return "100"


def process_message(message):
	sender_id = parser.parse_json(message, "sender", "id")
	recipient_id = parser.parse_json(message, "recipient", "id")
	message_body = parser.parse_json(message, "message")
	postback_body = parser.parse_json(message, "postback")

	if not sender_id:
		print "ERROR - no sender"
		return

	if not recipient_id:
		print "ERROR - no recipient"
		return

	if recipient_id != PAGE_ID:
		print "ERROR - not for me"
		return

	if postback_body:
		process_postback(sender_id, postback_body)
		return

	attachments = parser.parse_json(message_body, "attachments")
	if attachments:
		for attachment in attachments:
			process_attachment(sender_id, attachment)


def process_attachment(sender_id, attachment):
	type = parser.parse_json(attachment, "type")
	payload_url = parser.parse_json(attachment, "payload", "url")
	if type != "image" or not payload_url:
		return

	# show typing
	bot_client.send_action(sender_id, "typing_on")

	# save file to local
	file_name = generate_image_file_name(payload_url)
	download_file_from_url(payload_url, get_file_directory(sender_id, DirectoryType.DIR_TEMP, file_name))

	# get image category probability
	category_probabilities = classification_manager.get_image_category_probabilities(file_name)
	most_probable_category = max(category_probabilities.iteritems(), key=operator.itemgetter(1))[0]
	highest_probability = category_probabilities[most_probable_category]
	is_confident = highest_probability >= CATEGORY_PROBABILITY_THRESHOLD

	if is_confident:
		#
		bot_client.send_button_message(sender_id, "I think this is a %s. Am I right?" % CAT_TO_NAME[most_probable_category], [
			{
				"type": "postback",
				"title": "Yes, you are right",
				"payload": generate_payload("image_recog", file_name, most_probable_category)
			}, {
				"type": "postback",
				"title": "NO! It is a legwear.",
				"payload": generate_payload("image_recog", file_name, 3 - most_probable_category)
			},
		])
	else:
		bot_client.send_button_message(sender_id, "I can't tell what this is. Can you help me with it?", [
			{
				"type": "postback",
				"title": "It is a top.",
				"payload": generate_payload("image_recog", file_name, most_probable_category)
			}, {
				"type": "postback",
				"title": "It is a legwear.",
				"payload": generate_payload("image_recog", file_name, 3 - most_probable_category)
			}, {
				"type": "postback",
				"title": "Forget about it.",
				"payload": generate_payload("image_recog", file_name, ImageCategory.CAT_NONE)
			}
		])

	bot_client.send_action(sender_id, "typing_off")


def generate_payload(type, id, data):
	return json.dumps({
		"type": type,
		"id": id,
		"data": data
	})


def generate_file_key(file_url):
	return misc.hash_string(file_url)


def generate_image_file_name(file_url):
	file_key = misc.hash_string(file_url)
	return "%s%s" % (file_key, misc.get_file_extension(file_url))


def process_postback(sender_id, postback):
	payload_serialized = parser.parse_json(postback, "payload")
	if not payload_serialized:
		pass

	# payload = decode_payload(payload_serialized)