from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from skimage import color, exposure, transform
import numpy as np
import classify,os
from PIL import Image

BOTTOM_CASUAL = 0
BOTTOM_FORMAL = 1
TOP_CASUAL = 2
TOP_FORMAL = 3

male_model = "model/male.ml"
#female_model = "model/female.ml"

male_predictor = classify.model 
male_predictor.load_weights(male_model)

#female_predictor = classify.model 
#female_predictor.load_weights(female_model)

# return class and a array of prob
def predict(image_path, gender):
    predictor = male_predictor
    if gender == "female":
        predictor = female_predictor
    img = Image.open(image_path).convert('RGB') 
    img = img.resize( (classify.IMAGE_SIZE,classify.IMAGE_SIZE), Image.ANTIALIAS)
    img.save(image_path)
    x = load_img(image_path)
    x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
    x = x.reshape((1,) + x.shape)
    c = predictor.predict_classes(x)
    out = predictor.predict_proba(x)
    return c, out


imageNames = ['data/test/bc.jpeg','data/test/bf.jpeg', 'data/test/tf.jpeg', 'data/test/tf.jpg']
def test():
    for imageName in imageNames:
        c, out = predict(imageName, 'male')
        print c, out

if __name__ == "__main__":
    test()
