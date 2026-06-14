import os

import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "data", "UCI_Credit_Card.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)


def main():
    df = pd.read_csv(DATA_PATH)

    target_col = "default.payment.next.month"

    # Удаляем ID как технический идентификатор
    X = df.drop(columns=[target_col, "ID"])
    y = df[target_col]

    feature_columns = X.columns.tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    # v1 = текущая (контрольная) модель
    model_v1 = GradientBoostingClassifier(random_state=42)
    model_v1.fit(X_train, y_train)

    # v2 = новая (тестовая) модель
    model_v2 = RandomForestClassifier(
        n_estimators=150,
        max_depth=8,
        min_samples_leaf=5,
        random_state=42,
        class_weight="balanced_subsample",
        n_jobs=-1,
    )
    model_v2.fit(X_train, y_train)

    # Сохранение
    joblib.dump(model_v1, os.path.join(MODELS_DIR, "model_v1.pkl"))
    joblib.dump(model_v2, os.path.join(MODELS_DIR, "model_v2.pkl"))
    joblib.dump(feature_columns, os.path.join(MODELS_DIR, "feature_columns.pkl"))

    # Метрики для документации
    for name, model in [("v1", model_v1), ("v2", model_v2)]:
        y_pred = model.predict(X_test)
        f1 = f1_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)

        print(f"{name}:")
        print(f"  F1-score:  {f1:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall:    {recall:.4f}")
        print()


if __name__ == "__main__":
    main()