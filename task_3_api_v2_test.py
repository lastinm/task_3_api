from fastapi.testclient import TestClient
from task_3_api_v2 import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Для получения результата от модели используйте в адресе /predict/"}


def test_read_predict_positive():
    response = client.post("/predict/", json={"text": "Ваши работники грубые и наглые!"})
    # json_data = response.json()
    assert response.status_code == 200
