from fastapi.testclient import TestClient
from fastapi import status

from main import app

client = TestClient(app)

def test_get_home_page():
    response = client.get("/home")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message":"Project home Grupo Peluche"}
