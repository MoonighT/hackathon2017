from const import ImageCategory
from const import Occasion
import predict


def get_image_category_probabilities(image_path, gender):
	'''
	return image category for image stored in the path
	:param image_path:
	:return:
	'''
	c, prob = predict.predict(image_path, gender)
	bottom_prob = prob[predict.BOTTOM_CASUAL] + prob[predict.BOTTOM_FORMAL]
	top_prob = prob[predict.TOP_CASUAL] + prob[predict.TOP_FORMAL]
	return {
		ImageCategory.CAT_TOP: top_prob,
		ImageCategory.CAT_BOTTOM: bottom_prob
	}


def get_image_occasion_probability(image_path, gender, occasion):
	c, prob = predict.predict(image_path, gender)
	result = 0.0
	if occasion == Occasion.FORMAL:
		result = prob[predict.BOTTOM_FORMAL] + prob[predict.TOP_FORMAL]	
        elif occasion == Occasion.CASUAL:
		result = prob[predict.BOTTOM_CASUAL] + prob[predict.TOP_CASUAL]
	else:
		result = 0.5
	return result
