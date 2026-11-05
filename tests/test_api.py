import io
import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_upscale_no_file(client):
    response = client.post('/upscale')
    assert response.status_code == 400


def test_upscale_with_file(client):
    data = {'file': (io.BytesIO(b'fake image'), 'test.png')}
    response = client.post('/upscale', data=data, content_type='multipart/form-data')
    assert response.status_code == 202
    assert 'task_id' in response.get_json()


def test_task_status(client):
    response = client.get('/tasks/nonexistent')
    assert response.status_code in [200, 500]