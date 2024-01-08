import tensorflow as tf
import cv2
import numpy as np


def predict_kidney_diesease(image_path):

    loaded_model = tf.keras.models.load_model('static/models/model_100.h5')

    image = cv2.imread(image_path)
    image = cv2.resize(image, (224, 224))
    image = np.expand_dims(image, axis=0)
    image = image / 255.0

    predictions = loaded_model.predict(image)

    class_names = {0: 'Cyst', 1: 'Normal', 2: 'Stone', 3: 'Tumor'}
    pred_id = np.argmax(predictions)
    predicted_class = class_names[pred_id]

    return predicted_class



