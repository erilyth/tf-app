import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image

class TFInference:
    def __init__(self):
        self.model = keras.models.load_model("tf_model.h5")

    def predict(self, input_img: Image) -> Image:
        # img is of shape (height, width, 3)
        img = np.asarray(input_img)
        orig_rows, orig_cols = img.shape[0:2]

        # img is of shape (128, 128, 3)
        img = tf.image.resize(img, (128, 128))
        # Normalize the input image.
        img = tf.cast(img, tf.float32) / 255.0

        # Call the model.
        # pred_probs are of shape (1, 128, 128, 3)
        pred_probs = self.model.predict(img[tf.newaxis, ...])
        # preds is of shape (1, 128, 128)
        preds = tf.argmax(pred_probs, axis=-1)
        # preds is now of shape (128, 128, 1)
        preds = tf.expand_dims(tf.squeeze(preds, axis=0), axis=-1)
        # preds is finally of shape (height, width, 1)
        preds = np.asarray(tf.image.resize(preds, (orig_rows, orig_cols), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR))

        # Give each class a color => Red = Animal, Black = Background, Green = Unsure 
        class_to_rgb_map = {0: (128, 0, 0), 1: (0, 0, 0), 2: (0, 128, 0)}

        # Create the final predictions RGB image from preds.
        preds_img = np.zeros((orig_rows, orig_cols, 3))
        for row in range(orig_rows):
            for col in range(orig_cols):
                preds_img[row, col, :] = class_to_rgb_map[preds[row, col, 0]]

        # Cast the image to uint8 and return it
        preds_img = preds_img.astype('uint8')
        preds_img = Image.fromarray(preds_img, "RGB")

        return preds_img