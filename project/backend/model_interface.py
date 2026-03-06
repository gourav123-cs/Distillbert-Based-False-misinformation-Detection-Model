"""
Model Interface - Locked to my_fake_news_model only.
Loads once at startup. No multi-model logic. Optimized inference.
"""

import os
import sys

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# ---------------------------------------------------------------------------
# STRICT MODEL LOCK - System uses ONLY this model. No dynamic model loading.
# ---------------------------------------------------------------------------
MODEL_NAME = "my_fake_news_model"
MODEL_PATH = os.path.realpath(
    os.path.join(os.path.dirname(__file__), "..", MODEL_NAME)
)

# Global model and tokenizer - loaded once, reused for all requests
tokenizer = None
model = None
_model_ready = False
_device = None


def _ensure_model_loaded():
    """Load model and tokenizer once at startup. Verify and log each step."""
    global tokenizer, model, _model_ready, _device

    if _model_ready:
        return

    print("[INFO] Checking model path…")
    if not os.path.isdir(MODEL_PATH):
        print(f"[ERROR] Model directory not found: {MODEL_PATH}")
        print("[ERROR] Server cannot start. Ensure my_fake_news_model exists in project root.")
        sys.exit(1)
    print("[INFO] Model path exists")

    print("[INFO] Loading tokenizer…")
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
    except Exception as e:
        print(f"[ERROR] Tokenizer load failed: {e}")
        sys.exit(1)
    print("[INFO] Tokenizer loaded successfully")

    print("[INFO] Loading model…")
    try:
        model = AutoModelForSequenceClassification.from_pretrained(
            MODEL_PATH, local_files_only=True
        )
    except Exception as e:
        print(f"[ERROR] Model load failed: {e}")
        sys.exit(1)
    print("[INFO] Model loaded successfully")

    model.eval()
    print("[INFO] Model set to evaluation mode")

    _device = next(model.parameters()).device
    print(f"[INFO] Device used: {_device}")

    print(f"[INFO] Using model: {MODEL_NAME}")
    print("[INFO] Backend ready for predictions")

    print("[CONFIRMED] System locked to model: my_fake_news_model")
    print("[CONFIRMED] Multi-model loading disabled")
    print("[CONFIRMED] Backend optimized and ready")

    _model_ready = True


# Load at module import (server startup)
_ensure_model_loaded()


def predict(text: str) -> str:
    """
    Run inference using the global model. No reload. Lightweight and fast.
    Returns "Real News" or "Fake News". Label 0 = Real, Label 1 = Fake.
    """
    if not _model_ready or model is None or tokenizer is None:
        raise RuntimeError("Model not loaded")

    text = (text or "").strip()
    if not text:
        raise ValueError("No text provided")

    print("[INFO] Received prediction request")
    print("[INFO] Running inference using my_fake_news_model")

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512,
    )

    with torch.no_grad():
        logits = model(**inputs).logits

    predicted_class = logits.argmax(dim=1).item()

    print("[INFO] Prediction completed successfully")

    if predicted_class == 0:
        return "Real News"
    return "Fake News"
