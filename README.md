# Интеграционное тестирование PostgreSQL с Pytest и Docker

## 🧾 Цель проекта
Демонстрация запуска интеграционных тестов для PostgreSQL через:
1. Запуск базы данных в Docker-контейнере
2. Тестирование через Pytest
3. Использование виртуального окружения Python

---

## 📦 Требования
- [Docker](https://docs.docker.com/engine/install/)
- [Python 3.8+](https://www.python.org/downloads/)
- Установленный `docker-compose`

---

## 🛠️ Настройка

### 1. Клонирование репозитория
```bash
git clone https://github.com/DinoWithPython/personal-test-postgres
cd personal-test-postgres
```

### 2. Виртуальное окружение
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

_____
## 🧪 Запуск тестов
### 1. Запуск PostgreSQL
```bash
docker-compose up -d  # в этом случае контейнеры запустятся в фоновом режиме, логи не видны в терминале
или

docker-compose up
```
### 2. Выполнение тестов
```bash
pytest tests/
```

Пример теста (tests/test_integration.py):
```python
import pytest
from psycopg2 import connect

@pytest.fixture(scope="module")
def db_connection():
    conn = connect(
        host="localhost",
        port=5432,
        user="testuser",
        password="testpass",
        database="testdb"
    )
    yield conn
    conn.close()

def test_database_connection(db_connection):
    assert db_connection.status == "transaction"
```
________
## 📁 Структура проекта
```
project-root/ 
├── docker-compose.yml 
├── requirements.txt 
├── pytest.ini                  # Файл с настройками для тестов
├── tests.log                   # Дополнительно логи выводятся в файл.
├── venv/ 
└── tests/ 
      └── test_integration.py
```
_________
## Логика расположения тестов
### 1. Файл `__init__.py` в папке `tests`
Содержит базовый класс для тестирования. В нем определяется, что делать при запуске тестов и что делать после их выполнения. Фактически это создание таблиц указанных в папке `test_data` в файле `schems.sql`. После успешного завершения тестов, схема `public` удаляется каскадно. Таким образом каждый новый тест не будет зависеть от предыдущих запусков или данных.
### 2. Папка `test_data`
Содержит базовые файл(ы) для тестирования. Типа создания схем и таблиц, какое-то наполнение псевдо-данными этих таблиц. Она связана с классом тестирования, поэтому изменения логики в ней, скорее всего должны находить отражение в базовом классе.
### 3. Папка `test_cases`
Сожержит файлы для тестирования со своими методами, классами и прочим, которые наследуются от базового класса.<br>
<br>
Такая структура проекта по идее даёт удобный скелет для будущих интеграционных тестов.
