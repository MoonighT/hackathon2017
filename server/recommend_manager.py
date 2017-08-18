from const import ImageCategory
from const import Occasion, Scenario
import json

RECOM_PATH = 'recommendation.json'

recommend = dict()

def load_recommend(data_file):
    jsonfile = open(data_file, 'r')
    #json_str = jsonfile.read()
    data = json.load(jsonfile)
    global recommend
    recommend = data['recommendation']

def get_image_recommend(scenario, category):
    gender = 'male'
    global recommend
    occasion = 'casual'
    if scenario in [Scenario.INTERVIEW, Scenario.WEDDING, Scenario.PRESENTATION]:
        occasion = 'formal'
    entry = recommend[gender][occasion][category]
    return entry

load_recommend(RECOM_PATH)

if __name__ == "__main__":
    load_recommend(RECOM_PATH)
    print get_image_recommend('casual', 'bottom')
