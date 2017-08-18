def parse_json(json_obj, *args):
	for arg in args:
		json_obj = json_obj.get(arg, None)
		if not json_obj:
			return None
	return json_obj
