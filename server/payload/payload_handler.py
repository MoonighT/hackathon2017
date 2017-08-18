import json
import os

from const import ImageCategory, DirectoryType
from payload import Payload
from utils import misc


def process_payload(user_id, payload_serialized):
	payload = decode_payload(payload_serialized)
	if not payload:
		return None
	return handle_payload(user_id, payload)


def decode_payload(payload_serialized):
	payload_dict = json.loads(payload_serialized)
	if "type" in payload_dict and "id" in payload_dict and "data" in payload_dict:
		return Payload(payload_dict)
	return None


def handle_payload(user_id, payload):
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
		return "OK"
	return None
