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
