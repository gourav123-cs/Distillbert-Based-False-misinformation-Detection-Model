# Fake News Detection System

A clean, modern web interface and Flask backend that uses a fine-tuned **DistilBERT** model to classify news text as **Real News** or **Fake News**.

---

## Project Structure

```
project/
├── backend/
│   ├── app.py              # Flask app, POST /predict endpoint
│   ├── model_interface.py  # Loads model from my_fake_news_model/, runs inference
│   └── requirements.txt    # Python dependencies
├── my_fake_news_model/     # Trained model (config, tokenizer, weights*)
│   ├── config.json
│   ├── tokenizer.json
│   ├── tokenizer_config.json
│   └── model.safetensors   # ⬇ Download separately (see below)
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── .gitignore
└── README.md
```

> \* `model.safetensors` (~255 MB) is **not** included in the repository.  
> Follow the steps below to obtain it.

---

## Dataset

The model was trained on fake-news datasets available on Kaggle:

1. [Fake and Real News Dataset](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset)
2. [Fake News Classification](https://www.kaggle.com/datasets/saurabhshahane/fake-news-classification)

> Datasets are **not** included in this repo because of their size.  
> If you need them for retraining, download them from Kaggle and place the CSV files in a `data/` folder at the project root.

---

## Prerequisites

- **Python 3.8+**
- A modern browser (Chrome, Firefox, Safari, Edge)

---

## Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd project
```

### 2. Create a virtual environment and install dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Download the trained model weights

The `model.safetensors` file (~255 MB) is too large for GitHub.

**Option A** — Download from the release / shared link provided by the author and place it at:

```
my_fake_news_model/model.safetensors
```

**Option B** — Retrain the model yourself using the Kaggle datasets above.

### 4. Run the Flask backend

```bash
cd backend
python app.py
```

You should see:

```
[INFO] Server running
 * Running on http://127.0.0.1:5003
```

Leave this terminal open.

### 5. Open the frontend

**Option A – Open the HTML file directly**

- Double-click `frontend/index.html`, or
- From terminal: `open frontend/index.html` (macOS)

**Option B – Use a simple local server (recommended to avoid CORS issues)**

```bash
cd frontend
python -m http.server 8080
```

Then open: **http://127.0.0.1:8080** in your browser.

---

## How to Use

1. Make sure the backend is running (`python app.py` in `backend/`).
2. Open the frontend in your browser.
3. Type or paste a news headline or article text into the input field.
4. Click **Predict** (or press Enter).
5. The result card will display: **Real News** or **Fake News**.

### Test the API directly (optional)

```bash
curl -X POST http://127.0.0.1:5003/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Some news headline here"}'
```

```json
{"prediction": "Real News"}
```

---

## Tech Stack

| Layer    | Technology                     |
| -------- | ------------------------------ |
| Model    | DistilBERT (HuggingFace)       |
| Frontend | HTML, CSS, Vanilla JavaScript  |
| Backend  | Python, Flask                  |
| API      | POST `/predict`, JSON in/out   |

---

## License

For educational use (e.g. B.Tech project).
