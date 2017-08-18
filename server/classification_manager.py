from const import ImageCategory


def get_image_category_probabilities(image_path):
	'''
	return image category for image stored in the path
	:param image_path:
	:return:
	'''
	return {
		ImageCategory.CAT_TOP: 0,
		ImageCategory.CAT_BOTTOM: 1
	}


def get_image_occasion_probability(image_path, gender, occasion):
	return 0.5
