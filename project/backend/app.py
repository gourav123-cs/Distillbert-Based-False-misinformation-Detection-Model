"""
Flask backend for Fake News Detection System.

Locked to my_fake_news_model only. No multi-model or dropdown logic.
POST /predict with JSON: {"text": "..."} → {"prediction": "Real News" | "Fake News"}
"""

import os

from flask import Flask, request, jsonify

from model_interface import predict

app = Flask(__name__)

try:
    from flask_cors import CORS
    CORS(app)
except ImportError:
    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response


@app.route("/predict", methods=["POST"])
def predict_route():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "No text provided"}), 400

    user_text = data.get("text")

    if user_text is None:
        return jsonify({"error": "No text provided"}), 400
    if not isinstance(user_text, str):
        return jsonify({"error": "'text' must be a string"}), 400
    if not user_text.strip():
        return jsonify({"error": "No text provided"}), 400

    try:
        result = predict(user_text)
        return jsonify({"prediction": result})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    print("[INFO] Server running")
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="127.0.0.1", port=5003, debug=debug_mode)
