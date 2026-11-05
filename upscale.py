import numpy as np
from PIL import Image
import io
import tensorflow as tf
import os

# Загружаем модель ОДИН раз при импорте модуля
MODEL_PATH = 'EDSR_x2.pb'
_model = None


def get_model():
    global _model
    if _model is None:
        _model = tf.keras.models.load_model(MODEL_PATH)
    return _model


def upscale(image_bytes: bytes) -> bytes:
    model = get_model()

    image = Image.open(io.BytesIO(image_bytes))
    image = image.convert('RGB')

    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    output = model.predict(img_array)[0]
    output = np.clip(output, 0, 1) * 255.0
    output = output.astype(np.uint8)

    result_image = Image.fromarray(output)

    output_buffer = io.BytesIO()
    result_image.save(output_buffer, format='PNG')
    output_buffer.seek(0)

    return output_buffer.getvalue()