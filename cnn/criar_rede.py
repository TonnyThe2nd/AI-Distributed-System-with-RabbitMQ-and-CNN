import os
import pandas as pd
import shutil
from PIL import Image
import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

clean_path = '/kaggle/input/datasets/tonnythe2nd/sobe-filho-da-puta/Fruit And Vegetable Diseases Dataset'

source_path = path

clean_path = '/kaggle/working/clean_dataset'

os.makedirs(clean_path, exist_ok=True)

valid_extensions = ('.jpg', '.jpeg', '.png')

for class_name in os.listdir(source_path):

    class_source = os.path.join(source_path, class_name)

    if not os.path.isdir(class_source):
        continue

    class_dest = os.path.join(clean_path, class_name)

    os.makedirs(class_dest, exist_ok=True)

    for file in os.listdir(class_source):

        if not file.lower().endswith(valid_extensions):
            continue

        src_file = os.path.join(class_source, file)

        try:

            image = tf.io.read_file(src_file)

            # usa decode_image universal
            image = tf.image.decode_image(image)

            shutil.copy(src_file, class_dest)

        except Exception as e:

            print(f'Ignorada: {src_file}')

IMG_SIZE = (224, 224)
BATCH_SIZE = 32

train_dataset = tf.keras.utils.image_dataset_from_directory(
    clean_path,
    validation_split=0.2,
    subset='training',
    seed=42,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

val_dataset = tf.keras.utils.image_dataset_from_directory(
    clean_path,
    validation_split=0.2,
    subset='validation',
    seed=42,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

class_names = train_dataset.class_names

AUTOTUNE = tf.data.AUTOTUNE

train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
val_dataset = val_dataset.prefetch(buffer_size=AUTOTUNE)

data_augmentation = keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.2),
    layers.RandomZoom(0.2),
])

base_model = tf.keras.applications.EfficientNetB0(
    include_top=False,
    weights=None,
    input_shape=(224, 224, 3)
)

model_path = '/kaggle/input/models/tonnythe2nd/transfer-model/tensorflow2/default/1/efficientnetb0_notop.h5'

base_model.load_weights(
    model_path
)

base_model.trainable = False

inputs = keras.Input(shape=(224, 224, 3))
x = layers.RandomFlip("horizontal")(inputs)
x = layers.RandomRotation(0.2)(x)
x = tf.keras.applications.efficientnet.preprocess_input(x)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.2)(x)
outputs = layers.Dense(
    len(class_names),
    activation='softmax'
)(x)

model = keras.Model(inputs, outputs)

model.compile(
    optimizer=tf.keras.optimizers.Adam(),
    
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    
    metrics=[
        tf.keras.metrics.SparseCategoricalAccuracy(
            name='accuracy'
        )
    ]
)

callbacks = [
    tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',      
        patience=5,              
        restore_best_weights=True,
        verbose=1),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.3,
        patience=3,
        min_lr=1e-6,
        verbose=1),
    tf.keras.callbacks.ModelCheckpoint(
        'best_model.keras',
        monitor='val_loss',
        save_best_only=True,
        verbose=1
    )
]

history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=50,
    callbacks=callbacks
)

from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

y_true = []
y_pred = []

for images, labels in val_dataset:

    predictions = model.predict(images, verbose=0)

    predicted_labels = np.argmax(predictions, axis=1)

    y_true.extend(labels.numpy())
    y_pred.extend(predicted_labels)

print(classification_report(
    y_true,
    y_pred,
    target_names=class_names
))