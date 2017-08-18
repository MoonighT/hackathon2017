import base64
import hashlib
import os
import shutil
import urlparse

import requests
from flask import app

import const


def hash_string(original_string):
	return base64.b32encode(hashlib.sha256(original_string).digest())


def get_file_extension(url):
	return os.path.splitext(urlparse.urlparse(url).path)[1]


def download_file_from_url(url, local_path):
	response = requests.get(url, stream=True)

	if response.status_code == 200:
		with open(local_path, 'wb') as f:
			response.raw.decode_content = True
			shutil.copyfileobj(response.raw, f)


def get_file_directory(user_id, sub_dir_name, file_name):
	user_dir = os.path.join(const.DIR_WARDROBE, user_id)
	if not os.path.exists(user_dir):
		os.makedirs(user_dir)
	sub_dir = os.path.join(user_dir, sub_dir_name)
	if not os.path.exists(sub_dir):
		os.makedirs(sub_dir)
	return os.path.join(sub_dir, file_name)
