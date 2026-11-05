from celery import Celery
import os
import uuid
from upscale import upscale
from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND, UPLOAD_FOLDER

celery_app = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery_app.task(bind=True)
def upscale_task(self, image_bytes):
    result = upscale(image_bytes)

    filename = f"{uuid.uuid4()}.png"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    with open(filepath, 'wb') as f:
        f.write(result)

    return {"file": filename}