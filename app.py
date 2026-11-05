from flask import Flask, request, jsonify, send_from_directory
from tasks import upscale_task
from config import UPLOAD_FOLDER
import os

app = Flask(__name__)


@app.route('/upscale', methods=['POST'])
def upscale_route():
    if 'file' not in request.files:
        return jsonify({'error': 'Нет файла'}), 400

    file = request.files['file']
    image_bytes = file.read()

    task = upscale_task.delay(image_bytes)
    return jsonify({'task_id': task.id}), 202


@app.route('/tasks/<task_id>', methods=['GET'])
def task_status(task_id):
    task = upscale_task.AsyncResult(task_id)

    if task.state == 'PENDING':
        return jsonify({'status': 'PENDING'}), 200
    elif task.state == 'SUCCESS':
        result = task.result
        return jsonify({
            'status': 'SUCCESS',
            'file_url': f'/processed/{result["file"]}'
        }), 200
    elif task.state == 'FAILURE':
        return jsonify({'status': 'FAILURE', 'error': str(task.info)}), 500
    else:
        return jsonify({'status': task.state}), 200


@app.route('/processed/<path:filename>', methods=['GET'])
def get_processed(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)