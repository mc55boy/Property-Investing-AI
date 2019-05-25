#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 09:03:42 2019

@author: coopy
"""
from PIL import Image, ImageFilter
import os
from os import listdir
from os.path import isfile, join
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions

from keras import backend as K
#import matplotlib.pyplot as plt
#import numpy as np

import dbHandler as db


BASE_DIR = "Pictures/"

IMG_SIZE = (200, 200)

allSaleProps = db.getAllSaleID()


for prop in allSaleProps:
    directory = BASE_DIR + str(prop) + "/"
    all_files = [directory + f for f in listdir(directory) if isfile(join(directory, f))]
    prop_price = db.getPrice(prop)

    #for file in all_files:
    #    if "epc" not in file and "floor" not in file:
    #        print(prop)


def create_cnn(width, height, depth, filters=(16, 32, 64), regress=False):
    # initialize the input shape and channel dimension, assuming
	# TensorFlow/channels-last ordering

	inputShape = (height, width, depth)
    chanDim = -1
    inputs = Input(shape=inputShape)

    # loop over the number of filters
    for (i, f) in enumerate(filters):
        # if this is the first CONV layer then set the input
        # appropriately
        if i == 0:
            x = inputs

        # CONV => RELU => BN => POOL
        x = Conv2D(f, (3, 3), padding="same")(x)
        x = Activation("relu")(x)
        x = BatchNormalization(axis=chanDim)(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)

        # flatten the volume, then FC => RELU => BN => DROPOUT
        x = Flatten()(x)
        x = Dense(16)(x)
        x = Activation("relu")(x)
        x = BatchNormalization(axis=chanDim)(x)
        x = Dropout(0.5)(x)

        # apply another FC layer, this one to match the number of nodes
        # coming out of the MLP
        x = Dense(4)(x)
        x = Activation("relu")(x)

        # check to see if the regression node should be added
        if regress:
            x = Dense(1, activation="linear")(x)

        # construct the CNN
        model = Model(inputs, x)

        # return the CNN
        return model
