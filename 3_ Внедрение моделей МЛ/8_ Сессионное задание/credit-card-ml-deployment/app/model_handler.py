import json
import logging
import os
from datetime import datetime

import joblib
import numpy as np


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODELS_DIR = os.path.join(BASE_DIR, "models")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOGS_DIR, "api.log")


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if hasattr(record, "extra_data"):
            log_record.update(record.extra_data)
        return json.dumps(log_record, ensure_ascii=False)


logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(JsonFormatter())
    logger.addHandler(file_handler)


def load_model(version: str = "v1"):
    model_path = os.path.join(MODELS_DIR, f"model_{version}.pkl")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Модель не найдена: {model_path}")
    return joblib.load(model_path)


def load_feature_columns():
    feature_path = os.path.join(MODELS_DIR, "feature_columns.pkl")
    if not os.path.exists(feature_path):
        raise FileNotFoundError(f"Файл признаков не найден: {feature_path}")
    return joblib.load(feature_path)


def preprocess_input(data: dict, feature_columns: list):
    missing = [col for col in feature_columns if col not in data]
    if missing:
        raise ValueError(f"Отсутствуют обязательные признаки: {missing}")

    features = np.array([[data[col] for col in feature_columns]], dtype=float)
    return features


def predict(model, features):
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]
    return int(prediction), float(probability)