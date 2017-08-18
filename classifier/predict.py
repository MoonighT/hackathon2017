from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from skimage import color, exposure, transform
import numpy as np
import classify
from PIL import Image

imageName = 'data/test/3.jpeg'

male_model = "model/male_model.ml"
female_model = "model/female_model.ml"

male_predictor = classify.model 
male_predictor.load_weights(male_model)

female_predictor = classify.model 
female_predictor.load_weights(female_model)

def test():
    lm = classify.model
    lm.load_weights("first_try.h5")
    img = Image.open(imageName).convert('RGB')
    img = img.resize( (150,150), Image.ANTIALIAS)
    img.save(imageName)
    x = load_img(imageName)
    x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
    x = x.reshape((1,) + x.shape)
    out = lm.predict_proba(x,32,1)
    print out

def predict(image_path, gender):
    predictor = male_predictor
    if gender == "female":
        predictor = female_predictor
    img = Image.open(image_path).convert('RGB') 
    img = img.resize( (150,150), Image.ANTIALIAS)
    img.save(image_path)
    x = load_img(image_path)
    x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
    x = x.reshape((1,) + x.shape)
    out = lm.predict_proba(x)

if __name__ == "__main__":
    test()
