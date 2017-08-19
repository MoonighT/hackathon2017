def get_file_url(file):
	parts = file.decode("utf-8").split("wardrobe")
	return "https://stylist.gaofeng.one/wardrobe/" + parts[1]
