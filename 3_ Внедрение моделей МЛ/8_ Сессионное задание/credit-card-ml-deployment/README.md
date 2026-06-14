# Разработка и внедрение сервиса прогнозирования дефолта по кредитным картам с контейнеризацией и A/B-тестированием

## Описание проекта

Цель проекта — разработать production-like сервис машинного обучения для прогнозирования вероятности дефолта по кредитным картам.

Проект охватывает полный цикл внедрения модели:

* обучение модели машинного обучения;
* сохранение и загрузка модели;
* предоставление предсказаний через REST API;
* контейнеризация с использованием Docker;
* обеспечение воспроизводимости окружения;
* логирование запросов и ответов;
* подготовка архитектуры к масштабированию;
* организация A/B-тестирования двух версий модели.

---

## Бизнес-контекст

Для банка важно заранее оценивать вероятность дефолта клиента по кредитной карте.

Результаты модели могут использоваться для:

* снижения финансовых потерь;
* поддержки принятия решений по выдаче кредитов;
* оценки кредитного риска;
* повышения качества кредитного портфеля.

---

## Используемый датасет

### UCI Credit Card Default Dataset

Набор данных содержит информацию о клиентах кредитных карт и факте возникновения дефолта.

Характеристики датасета:

* Количество объектов: 30000
* Количество признаков: 24
* Тип задачи: бинарная классификация

Целевая переменная:

```text
default.payment.next.month
```

Значения:

```text
0 — клиент не ушёл в дефолт
1 — клиент ушёл в дефолт
```

---

## Используемые модели

В проекте используются две версии модели.

### Контрольная модель (v1)

```text
GradientBoostingClassifier
```

Используется в качестве текущей версии модели.

### Тестовая модель (v2)

```text
RandomForestClassifier
```

Используется для проведения A/B-тестирования.

---

## Архитектура решения

```text
Клиент
   │
   ▼
Flask API
   │
   ▼
Model Loader
   │
   ├── model_v1.pkl
   └── model_v2.pkl
   │
   ▼
Prediction
   │
   ▼
JSON Response
```

---

## Структура проекта

```text
credit-card-ml-deployment/
│
├── app/
│   ├── __init__.py
│   ├── api.py
│   └── model_handler.py
│
├── data/
│   └── UCI_Credit_Card.csv
│
├── models/
│   ├── train_model.py
│   ├── model_v1.pkl
│   ├── model_v2.pkl
│   └── feature_columns.pkl
│
├── tests/
│   └── test_api.py
│
├── docker/
│   └── Dockerfile
│
├── logs/
│
├── README.md
├── ARCHITECTURE.md
├── ab_test_plan.md
├── requirements.txt
├── docker-compose.yml
└── .gitignore
```

---

## Назначение основных файлов

| Файл                | Назначение                 |
| ------------------- | -------------------------- |
| api.py              | Flask API                  |
| model_handler.py    | Загрузка модели и инференс |
| train_model.py      | Обучение моделей           |
| model_v1.pkl        | Контрольная модель         |
| model_v2.pkl        | Тестовая модель            |
| feature_columns.pkl | Список признаков           |
| Dockerfile          | Контейнеризация            |
| docker-compose.yml  | Оркестрация сервисов       |
| ARCHITECTURE.md     | Архитектурное описание     |
| ab_test_plan.md     | План A/B-теста             |

---

# Установка зависимостей

## Создание виртуального окружения

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

## Установка зависимостей

```bash
pip install -r requirements.txt
```

---

# Обучение моделей

Перед первым запуском API необходимо обучить модели.

```bash
python models/train_model.py
```

После выполнения будут созданы файлы:

```text
models/model_v1.pkl
models/model_v2.pkl
models/feature_columns.pkl
```

---

# Запуск сервиса локально

Запуск Flask API:

```bash
python -m app.api
```

Сервис будет доступен по адресу:

```text
http://127.0.0.1:5000
```

---

# API

## Проверка работоспособности

### GET /health

Запрос:

```bash
curl http://127.0.0.1:5000/health
```

Ответ:

```json
{
  "status": "healthy"
}
```

---

## Получение предсказания

### POST /predict

Формат запроса:

```json
{
  "model_version": "v1",
  "features": {
    "LIMIT_BAL": 20000,
    "SEX": 2,
    "EDUCATION": 2,
    "MARRIAGE": 1,
    "AGE": 24,
    "PAY_0": 2,
    "PAY_2": 2,
    "PAY_3": -1,
    "PAY_4": -1,
    "PAY_5": -2,
    "PAY_6": -2,
    "BILL_AMT1": 3913,
    "BILL_AMT2": 3102,
    "BILL_AMT3": 689,
    "BILL_AMT4": 0,
    "BILL_AMT5": 0,
    "BILL_AMT6": 0,
    "PAY_AMT1": 0,
    "PAY_AMT2": 689,
    "PAY_AMT3": 0,
    "PAY_AMT4": 0,
    "PAY_AMT5": 0,
    "PAY_AMT6": 0
  }
}
```

---

### Пример запроса

```bash
curl -X POST http://127.0.0.1:5000/predict ^
-H "Content-Type: application/json" ^
-d "{\"model_version\":\"v1\",\"features\":{\"LIMIT_BAL\":20000,\"SEX\":2,\"EDUCATION\":2,\"MARRIAGE\":1,\"AGE\":24,\"PAY_0\":2,\"PAY_2\":2,\"PAY_3\":-1,\"PAY_4\":-1,\"PAY_5\":-2,\"PAY_6\":-2,\"BILL_AMT1\":3913,\"BILL_AMT2\":3102,\"BILL_AMT3\":689,\"BILL_AMT4\":0,\"BILL_AMT5\":0,\"BILL_AMT6\":0,\"PAY_AMT1\":0,\"PAY_AMT2\":689,\"PAY_AMT3\":0,\"PAY_AMT4\":0,\"PAY_AMT5\":0,\"PAY_AMT6\":0}}"
```

---

### Пример ответа

```json
{
  "prediction": 0,
  "probability": 0.1734,
  "model_version": "v1"
}
```

Описание ответа:

| Поле          | Описание                     |
| ------------- | ---------------------------- |
| prediction    | Предсказанный класс          |
| probability   | Вероятность дефолта          |
| model_version | Использованная версия модели |

---

# Тестирование API

Запуск тестов:

```bash
pytest tests/test_api.py
```

---

# Docker

## Сборка Docker-образа

```bash
docker build -t credit-card-ml-service:latest -f docker/Dockerfile .
```

---

## Запуск Docker-контейнера

```bash
docker run -p 5000:5000 credit-card-ml-service:latest
```

После запуска сервис будет доступен:

```text
http://localhost:5000
```

---

# Docker Compose

Запуск всех сервисов:

```bash
docker compose up --build
```

Запускаемые сервисы:

* ml-service
* nginx-demo

---

# Логирование

Все запросы и ответы API логируются.

Файл логов:

```text
logs/api.log
```

Формат логов:

```json
{
  "timestamp": "2026-06-15T12:00:00",
  "endpoint": "/predict",
  "model_version": "v1",
  "prediction": 0,
  "probability": 0.17
}
```

---

# A/B-тестирование

В проекте предусмотрена поддержка двух версий модели:

* v1 — контрольная группа;
* v2 — тестовая группа.

Подробный план тестирования находится в файле:

```text
ab_test_plan.md
```

---

# Архитектурные решения

Подробное описание:

```text
ARCHITECTURE.md
```

Файл содержит:

* монолит vs микросервисы;
* RabbitMQ;
* логирование;
* мониторинг;
* DVC;
* MLflow;
* ONNX;
* uWSGI + NGINX.

---

# Воспроизводимость проекта

Для полного воспроизведения проекта:

1. Клонировать репозиторий.
2. Создать виртуальное окружение.
3. Установить зависимости.
4. Обучить модели.
5. Запустить API.
6. Проверить работу эндпоинтов.
7. Собрать Docker-образ.
8. Запустить контейнер.

---

# Демонстрация работы

После запуска необходимо приложить:

* скриншот работы `/health`;
* скриншот работы `/predict`;
* скриншот или лог Docker-контейнера.

---

# Docker Hub

Ссылка на опубликованный Docker-образ:

```text
https://hub.docker.com/r/<your_dockerhub_username>/credit-card-ml-service
```

После публикации заменить на фактическую ссылку.

---

# Артефакты проекта

Репозиторий содержит:

* исходный код;
* обученные модели;
* Dockerfile;
* docker-compose.yml;
* requirements.txt;
* README.md;
* ARCHITECTURE.md;
* ab_test_plan.md;
* тесты API.

---

# Автор

Итоговый проект по дисциплине:

```text
Внедрение моделей машинного обучения
```
