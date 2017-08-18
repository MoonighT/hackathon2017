from const import ImageCategory
from const import Occasion, Scenario
import predict


def get_image_category_probabilities(image_path):
	'''
	return image category for image stored in the path
	:param image_path:
	:return:
	'''
	print image_path
	gender = 'male'
	c, prob = predict.predict(image_path, gender)
	#bottom_prob = prob[predict.BOTTOM_CASUAL] + prob[predict.BOTTOM_FORMAL]
	#top_prob = prob[predict.TOP_CASUAL] + prob[predict.TOP_FORMAL]
	bottom_prob = prob[predict.IS_BOTTOM]
	top_prob = prob[predict.IS_TOP]
	return {
		ImageCategory.CAT_TOP: top_prob,
		ImageCategory.CAT_BOTTOM: bottom_prob
	}

def get_image_occasion_probability(image_path, gender, scenario):
	gender = 'male'
	c, prob = predict.predict(image_path, gender)
	result = 0.0
	occasion = Occasion.CASUAL
	if scenario in [Scenario.INTERVIEW, Scenario.WEDDING, Scenario.DATE_NIGHT, Scenario.PRESENTATION]:
		occasion = Occasion.FORMAL
	if occasion == Occasion.FORMAL:
		result = prob[predict.BOTTOM_FORMAL] + prob[predict.TOP_FORMAL]
	elif occasion == Occasion.CASUAL:
		result = prob[predict.BOTTOM_CASUAL] + prob[predict.TOP_CASUAL]
	else:
		result = 0.5
	return result
