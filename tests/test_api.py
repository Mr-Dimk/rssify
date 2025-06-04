import pytest
from fastapi.testclient import TestClient
from app.main import app
import requests
import requests_mock

client = TestClient(app)

@pytest.fixture
def mock_requests():
    with requests_mock.Mocker() as m:
        # Пример: мок для внешнего запроса, который делает скрапер
        m.get("https://www.anthropic.com/claude-explains", text="<html><body><h2>Test Post</h2><p>Test Desc</p><a href='https://example.com/post'></a></body></html>")
        yield m

def test_check_site_with_mocked_scraping(mock_requests):
    # Предполагается, что сайт с id=1 уже есть в тестовой БД
    response = client.post("/api/sites/1/check")
    assert response.status_code == 200
    # Проверяем, что внешний запрос был сделан
    assert mock_requests.called
    # Проверяем, что результат содержит ожидаемое сообщение
    assert response.json()["detail"].startswith("Check started")
