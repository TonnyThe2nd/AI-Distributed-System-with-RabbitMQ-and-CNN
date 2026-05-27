import tensorflow as tf
import numpy as np


class Cnn:

    def __init__(self, model_path):

        self.modelo = tf.keras.models.load_model(model_path)

        self.classes = {
            0: "Maçã Saudável",
            1: "Maçã Podre",

            2: "Banana Saudável",
            3: "Banana Podre",

            4: "Pimentão Saudável",
            5: "Pimentão Podre",

            6: "Cenoura Saudável",
            7: "Cenoura Podre",

            8: "Pepino Saudável",
            9: "Pepino Podre",

            10: "Uva Saudável",
            11: "Uva Podre",

            12: "Goiaba Saudável",
            13: "Goiaba Podre",

            14: "Jujuba Saudável",
            15: "Jujuba Podre",

            16: "Manga Saudável",
            17: "Manga Podre",

            18: "Laranja Saudável",
            19: "Laranja Podre",

            20: "Romã Saudável",
            21: "Romã Podre",

            22: "Batata Saudável",
            23: "Batata Podre",

            24: "Morango Saudável",
            25: "Morango Podre",

            26: "Tomate Saudável",
            27: "Tomate Podre"
        }

    def preprocess_image(self, image_path):

        image = tf.keras.utils.load_img(
            image_path,
            target_size=(224, 224)
        )

        image = tf.keras.utils.img_to_array(image)

        image = tf.keras.applications.efficientnet.preprocess_input(image)

        return image

    def predict_image(self, image_path):

        image = self.preprocess_image(image_path)

        image = tf.expand_dims(image, axis=0)

        predictions = self.modelo.predict(image, verbose=0)

        predicted_class = np.argmax(predictions[0])

        confidence = np.max(predictions[0])

        return {
            'indice': int(predicted_class),
            'classe': self.classes[predicted_class],
            'confianca': float(confidence)
        }