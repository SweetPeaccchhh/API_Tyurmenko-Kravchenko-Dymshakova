# тесты для API-калькулятора
# запускаются автоматически в пайплайне GitHub Actions при каждом push

import pytest
from fastapi.testclient import TestClient

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app

client = TestClient(app)

# Корневые эндпоинты

def test_root():
    # Корневой эндпоинт возвращает статус ok
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "calculator-api"
    assert data["version"] == "1.0.0"


def test_health():
    # Healthcheck возвращает healthy
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

# базовые арифметические операции

def test_add():
    response = client.get("/add?a=2&b=3")
    assert response.status_code == 200
    assert response.json()["result"] == 5


def test_sub():
    response = client.get("/sub?a=5&b=2")
    assert response.status_code == 200
    assert response.json()["result"] == 3


def test_mul():
    response = client.get("/mul?a=4&b=3")
    assert response.status_code == 200
    assert response.json()["result"] == 12


def test_div():
    response = client.get("/div?a=10&b=2")
    assert response.status_code == 200
    assert response.json()["result"] == 5


def test_div_by_zero():
    # деление на ноль - ошибка 400
    response = client.get("/div?a=10&b=0")
    assert response.status_code == 400

# Расширенные операции

def test_pow():
    response = client.get("/v1/pow?a=2&b=10")
    assert response.status_code == 200
    assert response.json()["result"] == 1024


def test_sqrt():
    response = client.get("/v1/sqrt?a=16")
    assert response.status_code == 200
    assert response.json()["result"] == 4


def test_sqrt_negative():
    # корень из отрицательного числа - ошибка 422
    response = client.get("/v1/sqrt?a=-1")
    assert response.status_code == 422


def test_mod():
    response = client.get("/v1/mod?a=10&b=3")
    assert response.status_code == 200
    assert response.json()["result"] == 1


def test_mod_by_zero():
    # остаток от деления на ноль - ошибка 400
    response = client.get("/v1/mod?a=10&b=0")
    assert response.status_code == 400

# валидация

def test_invalid_input():
    # нечисловой параметр - ошибка 422
    response = client.get("/add?a=abc&b=3")
    assert response.status_code == 422


def test_missing_param():
    # отсутствующий параметр - ошибка 422
    response = client.get("/add?a=2")
    assert response.status_code == 422


def test_number_too_large():
    # число больше MAX_NUMBER - ошибка 422
    response = client.get("/v1/pow?a=1e10&b=10")
    assert response.status_code == 422