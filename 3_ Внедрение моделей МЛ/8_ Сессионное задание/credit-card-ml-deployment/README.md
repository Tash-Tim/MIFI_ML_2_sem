# Разработка и внедрение сервиса прогнозирования дефолта по кредитным картам с контейнеризацией и A/B-тестированием

## Описание проекта

Цель проекта — разработать production-like сервис машинного обучения для прогнозирования дефолта по кредитным картам, включающий полный цикл внедрения модели:

* обучение модели;
* сохранение и загрузка модели;
* предоставление REST API;
* контейнеризацию с использованием Docker;
* воспроизводимость окружения;
* логирование;
* архитектурное проектирование;
* A/B-тестирование нескольких версий модели.

Проект выполнен в рамках дисциплины:

```text
Внедрение моделей машинного обучения
```

---

# Бизнес-задача

Банку необходимо заранее оценивать вероятность дефолта клиента по кредитной карте.

Модель позволяет:

* снижать финансовые потери;
* повышать качество кредитного портфеля;
* поддерживать принятие решений по кредитным заявкам;
* автоматизировать оценку кредитного риска.

---

# Используемый датасет

Используется датасет:

```text
UCI Credit Card Default Dataset
```

Характеристики:

| Параметр             | Значение               |
| -------------------- | ---------------------- |
| Количество объектов  | 30000                  |
| Количество признаков | 24                     |
| Тип задачи           | Бинарная классификация |

Целевая переменная:

```text
default.payment.next.month
```

Значения:

```text
0 — отсутствует дефолт
1 — дефолт
```

---

# Используемые модели

В проекте реализованы две версии модели.

## Контрольная модель (v1)

```text
GradientBoostingClassifier
```

Используется как текущая версия сервиса.

---

## Тестовая модель (v2)

```text
RandomForestClassifier
```

Используется для A/B-тестирования.

---

# Архитектура решения

Общая схема:

```text
Client
   │
   ▼
Flask API
   │
   ▼
Model Handler
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

Подробное описание архитектуры приведено в файле:

```text
ARCHITECTURE.md
```

---

# Структура репозитория

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

# Установка зависимостей

## Создание виртуального окружения

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

---

## Установка зависимостей

```powershell
pip install -r requirements.txt
```

---

# Обучение моделей

Перед первым запуском необходимо обучить модели:

```powershell
python models\train_model.py
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

```powershell
python -m app.api
```

После запуска сервис будет доступен:

```text
http://127.0.0.1:5000
```

---

# API

## Проверка работоспособности

### GET /health

Проверка через браузер:

```text
http://127.0.0.1:5000/health
```

Ожидаемый ответ:

```json
{
  "status": "healthy"
}
```

---

## Получение предсказания

### POST /predict

Пример запроса:

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

Пример ответа:

```json
{
  "prediction": 1,
  "probability": 0.7553,
  "model_version": "v1"
}
```

---

# Тестирование API

Запуск тестов:

```powershell
pytest tests\test_api.py
```

Ожидаемый результат:

```text
3 passed
```

---

# Воспроизводимость проекта

Для полного воспроизведения проекта необходимо:

1. Клонировать репозиторий.
2. Создать виртуальное окружение.
3. Установить зависимости.
4. Обучить модели.
5. Запустить Flask API.
6. Проверить endpoint `/health`.
7. Проверить endpoint `/predict`.
8. Выполнить тестирование API.
9. Собрать Docker-образ.
10. Запустить Docker-контейнер.

---

# Docker

## Сборка Docker-образа

Из корня проекта:

```powershell
docker build -t credit-card-ml-service:latest -f docker\Dockerfile .
```

---

## Запуск контейнера

```powershell
docker run -p 5000:5000 credit-card-ml-service:latest
```

После запуска:

```text
http://127.0.0.1:5000
```

---

## Проверка контейнера

Проверка endpoint:

```text
http://127.0.0.1:5000/health
```

Ожидаемый ответ:

```json
{
  "status": "healthy"
}
```

---

# Docker Compose

Запуск всех сервисов:

```powershell
docker compose up --build
```

Остановка:

```powershell
docker compose down
```

---

# Логирование

Логи сохраняются в:

```text
logs/api.log
```

Формат логов:

```json
{
  "timestamp": "2026-06-15T12:00:00",
  "endpoint": "/predict",
  "model_version": "v1",
  "prediction": 1,
  "probability": 0.75
}
```

Логируются:

* запросы;
* ответы;
* ошибки;
* используемая версия модели.

Подробное описание находится в:

```text
ARCHITECTURE.md
```

---

# A/B-тестирование

В проекте реализована поддержка двух моделей:

```text
v1 — контрольная группа
v2 — тестовая группа
```

Переключение осуществляется через параметр:

```json
{
  "model_version": "v1"
}
```

или

```json
{
  "model_version": "v2"
}
```

Подробный план тестирования находится в:

```text
ab_test_plan.md
```

---

# Демонстрация работы

Для подтверждения работоспособности,в папке "1_ screenshot reports", проекта приложены:

* 01_Тестирование_API_3_passed.jpg;
* 02_Эндпоинт_predict.jpg;
* 03_Сборка_Docker_образа.jpg;
* 04_Запуск_Docker_контейнера.jpg;
* 05_Проверка_health_через_PowerShell.jpg
* 06_Проверка_health_через_браузер.jpg.

---

# Docker Hub

Ссылка на опубликованный Docker-образ:

```text
https://hub.docker.com/repository/docker/tnazarov1991/mifi-ml-session-credit-card-mldepl/general
```


---

# Артефакты проекта

Проект содержит:

* исходный код;
* обученные модели;
* requirements.txt;
* Dockerfile;
* docker-compose.yml;
* README.md;
* ARCHITECTURE.md;
* ab_test_plan.md;
* тесты API.

---

# Автор: Назаров Темур

Итоговый проект по дисциплине:

```text
Внедрение моделей машинного обучения
```
