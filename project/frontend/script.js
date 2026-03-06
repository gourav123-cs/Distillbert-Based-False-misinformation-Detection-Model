/**
 * Fake News Detection System - Frontend
 *
 * Sends user text to backend POST /predict and displays the response.
 * No prediction logic here; all analysis is done on the backend.
 */

(function () {
  "use strict";

  const API_URL = "http://127.0.0.1:5003/predict";

  const textInput = document.getElementById("text-input");
  const predictBtn = document.getElementById("predict-btn");
  const loadingEl = document.getElementById("loading");
  const resultCard = document.getElementById("result-card");
  const resultValue = document.getElementById("result-value");

  /**
   * Show loading spinner and hide result card.
   */
  function showLoading() {
    loadingEl.classList.add("is-visible");
    resultCard.classList.remove("is-visible");
    resultCard.classList.add("result-card--hidden");
  }

  /**
   * Hide loading spinner.
   */
  function hideLoading() {
    loadingEl.classList.remove("is-visible");
  }

  /**
   * Display prediction result with a smooth fade-in.
   */
  function showResult(prediction) {
    resultValue.textContent = prediction;
    resultCard.classList.remove("result-card--hidden");
    // Force reflow so animation runs
    resultCard.offsetHeight;
    resultCard.classList.add("is-visible");
  }

  /**
   * Show an error message in the result area.
   */
  function showError(message) {
    resultValue.textContent = message;
    resultCard.classList.remove("result-card--hidden");
    resultCard.offsetHeight;
    resultCard.classList.add("is-visible");
  }

  /**
   * Call backend /predict and update UI.
   */
  async function runPrediction() {
    const text = (textInput.value || "").trim();

    if (!text) {
      showError("Please enter some text first.");
      return;
    }

    showLoading();
    predictBtn.disabled = true;

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: text }),
      });

      const data = await response.json().catch(function () {
        return { prediction: "Invalid response from server." };
      });

      hideLoading();

      if (!response.ok) {
        showError(data.error || "Request failed.");
        return;
      }

      if (typeof data.prediction !== "string") {
        showError("Unexpected response format.");
        return;
      }

      showResult(data.prediction);
    } catch (err) {
      hideLoading();
      showError("Could not reach the server. Is the Flask backend running on port 5003?");
    } finally {
      predictBtn.disabled = false;
    }
  }

  /**
   * Predict on button click.
   */
  predictBtn.addEventListener("click", runPrediction);

  /**
   * Optional: Predict on Enter key in the input.
   */
  textInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      runPrediction();
    }
  });
})();
