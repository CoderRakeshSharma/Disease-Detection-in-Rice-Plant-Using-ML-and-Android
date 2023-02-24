# -*- coding: utf-8 -*-
from __future__ import division, print_function

#import sys
import os
#import glob
#import re
import numpy as np

# Keras
from keras.models import load_model
from keras.utils import load_img, img_to_array
# from tensorflow.keras.utils import load_img
# from keras.preprocessing import image
from keras_preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGI
#from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

model = load_model("CnnModel.h5")
        # Necessary
# print('Model loaded. Start serving...')




def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224,224))

    # Preprocessing the image
    x = image.img_to_array(img)
    x = np.true_divide(x, 255)
    #x= x/255.0
    y_pred=model.predict(x.reshape(1,224,224,3))
    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    preds = y_pred
    
    str1=''
    
    result=np.argmax(preds,axis=1) #take the index value of that array which value is maximum
    
    if result==0:
       str1='Bacterial Leaf Blight'
       
    elif result==1:
       str1='Brownspot'
       
    elif result==2:
       str1='WOW IT IS A HEALTHY PLANT'
       
    elif result==3:
       str1='Leafsmut'
         
    else:
       str1="IMAGE IS NOT MATCHING"
       
    return str1


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'SAMPLE DATA', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)


        return preds
    return None


if __name__ == '__main__':
    app.run() #debug=True)