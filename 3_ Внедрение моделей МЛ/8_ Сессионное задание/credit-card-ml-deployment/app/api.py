from flask import Flask, jsonify, request

from app.model_handler import (
    load_feature_columns,
    load_model,
    logger,
    predict,
    preprocess_input,
)

app = Flask(__name__)

feature_columns = load_feature_columns()
models = {
    "v1": load_model("v1"),
    "v2": load_model("v2"),
}


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/predict", methods=["POST"])
def predict_endpoint():
    """
    Формат запроса:
    {
      "model_version": "v1",
      "features": {
        "LIMIT_BAL": 20000,
        "SEX": 2,
        ...
      }
    }

    Формат ответа:
    {
      "prediction": 1,
      "probability": 0.7345,
      "model_version": "v1"
    }
    """
    try:
        data = request.get_json()

        if not data or "features" not in data:
            return jsonify({"error": "JSON должен содержать поле 'features'"}), 400

        model_version = data.get("model_version", "v1")
        if model_version not in models:
            return jsonify({"error": "Допустимые версии модели: v1, v2"}), 400

        features = preprocess_input(data["features"], feature_columns)
        prediction, probability = predict(models[model_version], features)

        response = {
            "prediction": prediction,
            "probability": probability,
            "model_version": model_version,
        }

        logger.info(
            "Prediction request processed",
            extra={
                "extra_data": {
                    "endpoint": "/predict",
                    "request_model_version": model_version,
                    "request_features": data["features"],
                    "response": response,
                }
            },
        )

        return jsonify(response), 200

    except Exception as e:
        logger.error(
            "Prediction request failed",
            extra={
                "extra_data": {
                    "endpoint": "/predict",
                    "error": str(e),
                }
            },
        )
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)