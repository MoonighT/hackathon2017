import json

from const import ImageCategory
from payload.payload import Payload


def process_payload(payload_serialized):
	payload = process_payload(payload_serialized)
	if not payload:
		pass


def decode_payload(payload_serialized):
	payload_dict = json.loads(payload_serialized)
	if "type" in payload_dict and "id" in payload_dict and "data" in payload_dict:
		return Payload(payload_dict)
	return None


def handle_payload(payload):
	if payload.type == "image_recog":
		if payload.data == ImageCategory.CAT_NONE:
			# remove image from temp
			pass