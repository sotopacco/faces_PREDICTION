# -*- coding: utf-8 -*-
"""Copia de CNN FACIAL.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RSIkEqe39UHhNp8ZGKYd3BgttwyNkZ-T
"""

import sys
import os
import numpy as np
import tensorflow as tf
from keras.models import load_model
import sklearn.metrics as metrics
from PIL import Image
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras import backend as K
from google.colab import drive
drive.mount('/content/drive')

K.clear_session()

data_entrenamiento = '/content/drive/My Drive/TCD/UII/P2/img_F_M/train'
data_test = '/content/drive/My Drive/TCD/UII/P2/img_F_M/test'

entrenamiento_datagen = ImageDataGenerator(rescale = 1./255,shear_range = 0.3,zoom_range = 0.3,horizontal_flip = True)
validacion_datagen = ImageDataGenerator(rescale = 1./255)
imagen_entrenamiento = entrenamiento_datagen.flow_from_directory(data_entrenamiento,target_size = (222, 222),batch_size = 32,class_mode = 'categorical')
imagen_validacion = validacion_datagen.flow_from_directory(	data_test,target_size=(222,222),batch_size=32,class_mode='categorical')

cnn = Sequential()
cnn.add(Convolution2D(32, (3,3), padding='same', input_shape=(222, 222,3), activation='relu'))
cnn.add(MaxPooling2D(pool_size=(2,2)))
cnn.add(Convolution2D(64, (2,2), padding='same', activation='relu'))
cnn.add(MaxPooling2D(pool_size=(2,2)))
cnn.add(Convolution2D(128, (3,3), padding='same', activation='relu'))
cnn.add(MaxPooling2D(pool_size=(2,2)))
cnn.add(Flatten())
cnn.add(Dense(512, activation='relu'))
cnn.add(Dense(256, activation='relu'))
#cnn.add(Dense(128, activation='relu'))
cnn.add(Dense(64, activation='relu'))
misclases = 2
cnn.add(Dense(misclases, activation='softmax'))

cnn.summary()

cnn.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

cnn.fit(imagen_entrenamiento, steps_per_epoch=10, epochs=200, validation_data=imagen_validacion, validation_steps=20)

score = cnn.evaluate(imagen_validacion)
print("Exactitud test:", score[1])

y_pred = cnn.predict(imagen_validacion)
y_pred_labels = np.argmax(y_pred, axis=1)
y_pred_labels

def Prediccion(ruta_imagen):
    x = tf.keras.preprocessing.image.load_img(ruta_imagen, target_size=(222, 222))
    x = tf.keras.preprocessing.image.img_to_array(x)
    x = np.expand_dims(x, axis=0)
    arreglo = cnn.predict(x)
    resultado = arreglo[0]
    respuesta = np.argmax(resultado)

    if respuesta == 0:
        print('Varon')
    elif respuesta == 1:
        print('Mujer')

    im = Image.open(ruta_imagen)
    plt.imshow(im)
    plt.axis('off')
    plt.show()

carpeta_imagenes = '/content/drive/My Drive/TCD/UII/P2/img_F_M/prediccion/'
for imagen_nombre in os.listdir(carpeta_imagenes):
    imagen_path = os.path.join(carpeta_imagenes, imagen_nombre)
    if os.path.isfile(imagen_path):
        print(f"Predicción para {imagen_nombre}:")
        Prediccion(imagen_path)