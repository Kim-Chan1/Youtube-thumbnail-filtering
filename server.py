from flask import Flask, request, jsonify
from http import HTTPStatus
from flask_cors import CORS
import requests
from PIL import Image
from io import BytesIO
import numpy as np
import tensorflow as tf
import torch
import os
import keras
import threading
from keras import ops
from keras import layers, models, preprocessing, Model, applications, utils

app = Flask(__name__)
CORS(app)
img_size = (224, 224)
i = 0
base_model = keras.applications.ResNet50(weights = 'imagenet', include_top=False, input_shape=img_size+(3,), pooling='avg')
base_model.trainable = False

# 가중치를 불러오기 때문에 Model 구성을 해준다.
input = keras.Input(shape=(224, 224, 3))
x = base_model(input, training = False)
x = layers.Dropout(0.5)(x)
outputs = layers.Dense(3, activation='softmax')(x)
model = Model(input, outputs)
model.load_weights('resnet50.h5')
i = 0
img_path = "./images"

classes = ["other", "skin", "tryphopobia", "insect", "deadbody"]

def preprocess_image(img_path, target_size=img_size):
    try:
        
        img = preprocessing.image.load_img(img_path, target_size = target_size)
        
        img_array = preprocessing.image.img_to_array(img)
        
        img_array = np.expand_dims(img_array, axis = 0)
        
        img_array /= 255.0
        
        return img_array
        
    except Exception as e:
        raise ValueError(f"Error Processing image from URL: {e}")

def predicted_image(url):
    global i
    try:
        if not os.path.isdir("./images"):
            os.makedirs("./images")
        
        with open("./images/"+ str(i) + ".jpg", 'wb') as img_file:
            img_response = requests.get(url)
            img_file.write(img_response.content)
        
        
        img_array = preprocess_image(img_path + f'/{i}.jpg')
        predictions = model.predict(img_array)
        predicted_class_idx = np.argmax(predictions, axis = -1)[0]
        predicted_class_label = classes[predicted_class_idx]
        i += 1
        return predicted_class_label
    except Exception as e:
        return str(e)


@app.route('/predict', methods=['POST'])
def predict():
    # Chrome Extension으로부터 URL을 받아옴.
    data = request.get_json()
    url = data['url']

    print("Recieved url : " , url)
    
    if(url != ''):
        try:
            result = predicted_image(url)
            print(result)
            return jsonify({'class': result})
        except Exception as e:
            return jsonify({"오류 발생": str(e)}), 500
         
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)