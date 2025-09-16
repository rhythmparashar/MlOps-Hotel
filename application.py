import os
import joblib
import numpy as np
from flask import Flask, render_template, request

from config.paths_config import MODEL_OUTPUT_PATH

app = Flask(__name__)

# Load the trained model
try:
    loaded_model = joblib.load(MODEL_OUTPUT_PATH)
except Exception as e:
    print(f"Error loading model: {e}")
    loaded_model = None

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    error_message = None

    if request.method == 'POST':
        try:
            # Extract input features from the form
            lead_time = int(request.form.get("lead_time", 0))
            no_of_special_request = int(request.form.get("no_of_special_request", 0))
            avg_price_per_room = float(request.form.get("avg_price_per_room", 0.0))
            arrival_month = int(request.form.get("arrival_month", 0))
            arrival_date = int(request.form.get("arrival_date", 0))
            market_segment_type = int(request.form.get("market_segment_type", 0))
            no_of_week_nights = int(request.form.get("no_of_week_nights", 0))
            no_of_weekend_nights = int(request.form.get("no_of_weekend_nights", 0))
            type_of_meal_plan = int(request.form.get("type_of_meal_plan", 0))
            room_type_reserved = int(request.form.get("room_type_reserved", 0))

            # Prepare features for prediction
            features = np.array([[lead_time, no_of_special_request, avg_price_per_room,
                                  arrival_month, arrival_date, market_segment_type,
                                  no_of_week_nights, no_of_weekend_nights,
                                  type_of_meal_plan, room_type_reserved]])

            # Make prediction
            if loaded_model is not None:
                prediction_value = loaded_model.predict(features)
                prediction = int(prediction_value[0])
            else:
                error_message = "Model not loaded."

        except Exception as e:
            error_message = f"Error during prediction: {e}"

    return render_template("index.html", prediction=prediction, error=error_message)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
