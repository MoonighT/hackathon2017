from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.models import Sequential
from keras.layers.core import Flatten, Dense, Dropout, Lambda
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.optimizers import SGD, Adam


def norm_input(x):
        return x

def ConvBlock(model, layers, filters):
        for i in range(layers):
                model.add(ZeroPadding2D((1,1)))
                model.add(Convolution2D(filters, 3, 3, activation='relu'))
                model.add(MaxPooling2D((2,2), strides=(1,1)))

def FCBlock(model):
        model.add(Dense(50, activation='relu'))

model = Sequential([Lambda(norm_input, input_shape=(128,128,3))])
ConvBlock(model,2,32)
ConvBlock(model,2,32)
ConvBlock(model,2,64)
ConvBlock(model,2,64)

model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors
#model.add(Dense(64))
#model.add(Activation('relu'))
model.add(Dropout(0.5))
#model.add(Dense(4))
#model.add(Activation('softmax'))
model.add(Dense(2, activation='softmax'))

model.compile(optimizer=Adam(), loss='categorical_crossentropy',
              metrics=['accuracy'])

batch_size = 10

# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)


# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator(rescale=1./255)

# this is a generator that will read pictures found in
# subfolers of 'data/train', and indefinitely generate
# batches of augmented image data
train_generator = train_datagen.flow_from_directory(
        'data/train',  # this is the target directory
        target_size=(128, 128),  # all images will be resized to 150x150
        batch_size=batch_size,
        class_mode='categorical')  

# this is a similar generator, for validation data
validation_generator = test_datagen.flow_from_directory(
        'data/validation',
        target_size=(128, 128),
        batch_size=batch_size,
        class_mode='categorical')

def train():
        model.optimizer.lr = 0.001
        model.fit_generator(
                train_generator,
                steps_per_epoch=500 // batch_size,
                epochs=10,
                validation_data=validation_generator,
                validation_steps=500 // batch_size)
        model.save_weights('model.h0')  # always save your weights after training or during training

if __name__ == "__main__":
        train()
