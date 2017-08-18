from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.layers.core import Flatten, Dense, Dropout, Lambda
from skimage import color, exposure, transform
import numpy as np
import classify, os
from PIL import Image

IS_BOTTOM = 0
IS_TOP = 1

IS_BEACH = 0
IS_FORMAL = 1

BOTTOM_CASUAL = 0
BOTTOM_FORMAL = 1
TOP_CASUAL = 2
TOP_FORMAL = 3

Dating = 0
Hackathon = 1
Interview = 2
Party = 3
Sports = 4
Wedding = 5


male_model = "model/category.ml"
male_predictor = classify.make_category_model()
male_predictor.add(Dropout(0.0))
male_predictor.load_weights(male_model)

occursion_model = "model/formal.ml"
occursion_predictor = classify.make_occursion_model()
occursion_predictor.add(Dropout(0.0))
occursion_predictor.load_weights(occursion_model)

# return class and a array of prob
def predict(image_path, gender):
    predictor = male_predictor
    img = Image.open(image_path).convert('RGB') 
    img = img.resize( (classify.CATEGORY_IMAGE_SIZE,classify.CATEGORY_IMAGE_SIZE), Image.ANTIALIAS)
    img.save(image_path+'.jpg')
    x = load_img(image_path+'.jpg')
    x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
    x = x.reshape((1,) + x.shape)
    c = predictor.predict_classes(x,verbose=0)
    out = predictor.predict_proba(x,verbose=0)
    os.remove(image_path+'.jpg')
    return c, out[0]

def predict_occursion(image_path, gender):
    predictor = occursion_predictor
    img = Image.open(image_path).convert('RGB') 
    img = img.resize( (classify.OCASSION_IMAGE_SIZE,classify.OCASSION_IMAGE_SIZE), Image.ANTIALIAS)
    img.save(image_path+'.jpg')
    x = load_img(image_path+'.jpg')
    x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
    x = x.reshape((1,) + x.shape)
    c = predictor.predict_classes(x,verbose=0)
    out = predictor.predict_proba(x,verbose=0)
    os.remove(image_path+'.jpg')
    return c, out[0]


def test():
    #imageNames = ['data/test/1.jpg', 'data/test/2.jpg', 'data/test/3.jpg', 'data/test/6.jpg', 'data/test/5.jpg']
    for i in range(38):
        imageName = 'data/test/'+str(i)+'.jpg'
        c, out = predict_occursion(imageName, 'male')
        print c, out

if __name__ == "__main__":
    test()
