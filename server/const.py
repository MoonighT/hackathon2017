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
	DATE_NIGHT = 5
	HACKATHON = 6
	PRESENTATION = 7


SCENARIO_DETAILS = {
	Scenario.INTERVIEW: {
		"title": "Job Interview",
		"subtitle": "Going for an interview? Try some of these outfits",
		"image_url": "https://blog.clutchprep.com/wp-content/uploads/2015/11/interview-pic.jpeg",
	},
	Scenario.PARTY: {
		"title": "Party",
		"subtitle": "Heading out for some fun? Try some of these outfits",
		"image_url": "http://www.begbrookclub.co.uk/o-CHRISTMAS-PARTY-570.jpg",
	},
	Scenario.WEDDING: {
		"title": "Wedding Ceremony",
		"subtitle": "Decent clothes for the BIG day? Try some of these outfits",
		"image_url": "https://wwcdn.weddingwire.com/assets/category-landings/inspiration_tiles/11/rustic-california-garden-wedding-685c40d3962159d56df7f1863a683530f88412e5ea3e3b30b83eeaacccd34067.jpg",
	},
	Scenario.PRESENTATION: {
		"title": "Presentation",
		"subtitle": "Impress the audience with some smart outfits? You should never miss these suggestions!",
		"image_url": "https://cdn2.hubspot.net/hubfs/580101/How%20to%20create%20a%20winning%20presentation-367141-edited.jpg",
	},
	Scenario.DATE_NIGHT: {
		"title": "Date Night",
		"subtitle": "Wow! You will look more impressive with these outfits!",
		"image_url": "http://www.rolereboot.org/wp-content/uploads/2014/08/date-night.jpg",
	},
	Scenario.HACKATHON: {
		"title": "Hackathon",
		"subtitle": "Jeans and hoodies? You won't go wrong with these options!",
		"image_url": "https://cdn.yourstory.com/wp-content/uploads/2015/01/Hackathon-2014.jpg",
	}
}
