import os

dir_path = os.path.dirname(os.path.realpath(__file__))
DIR_WARDROBE = os.path.join(dir_path, "wardrobe")


class ImageCategory(object):
	CAT_NONE = 0
	CAT_TOP = 1
	CAT_BOTTOM = 2


CAT_TO_NAME = {
	ImageCategory.CAT_TOP: "Top",
	ImageCategory.CAT_BOTTOM: "Legwear"
}

class DirectoryType(object):
	DIR_TEMP = "temp"
	DIR_TOP = "top"
	DIR_BOTTOM = "bottom"


class Gender(object):
	MALE = 1
	FEMALE = 2


class Occasion(object):
	FORMAL = 1
	CASUAL = 2


class Scenario(object):
	INTERVIEW = 1
	PARTY = 2
	WEDDING = 3
	PRESENTATION = 4
	DATE_NIGHT = 5
	HACKATHON = 6


SCENARIO_DETAILS = {
	Scenario.INTERVIEW: {
		"title": "Job Interview",
		"subtitle": "Going for an interview? Try some of these outfits",
	},
	Scenario.PARTY: {
		"title": "Party",
		"subtitle": "Heading out for some fun? Try some of these outfits",
	},
	Scenario.WEDDING: {
		"title": "Wedding Ceremony",
		"subtitle": "Decent clothes for the BIG day? Try some of these outfits",
	},
	Scenario.PRESENTATION: {
		"title": "Presentation",
		"subtitle": "Impress the audience with some smart outfits? You should never miss these suggestions!",
	},
	Scenario.DATE_NIGHT: {
		"title": "Date Night",
		"subtitle": "Wow! You will look more impressive with these outfits!",
	},
	Scenario.HACKATHON: {
		"title": "Hackathon",
		"subtitle": "Sweat pants and hoodies? You won't go wrong with these options!"
	}
}
