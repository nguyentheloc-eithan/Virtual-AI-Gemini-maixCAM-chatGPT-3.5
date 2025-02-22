# main.py
import os
import io
import cv2
import numpy as np
from flask import Flask, request, jsonify
from fall_service import FallService
from notification_service import NotificationService

# Configuration values
MODEL_PATH ="Model_is_still_training" 
TELEGRAM_BOT_TOKEN = "TELEGRAM_BOT_TOKEN"  
TELEGRAM_CHAT_ID = "TELEGRAM_CHAT_ID"      

# Initialize services
fall_service = FallService(model_path=MODEL_PATH, input_size=(224, 224), threshold=0.5)
notifier = NotificationService(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)

# Create Flask app
app = Flask(__name__)

@app.route("/detect_fall", methods=["POST"])
def detect_fall_api():
    """
    Expects an image file uploaded with the key 'image'. The endpoint:
      - Reads the image,
      - Runs fall detection on it,
      - Sends a Telegram alert if a fall is detected,
      - Returns a JSON response indicating the result.
    """
    if "image" not in request.files:
        return jsonify({"error": "Image file is required with key 'image'."}), 400

    image_file = request.files["image"]
    # Read image file data into a numpy array
    image_bytes = image_file.read()
    # Convert bytes to numpy array and decode using OpenCV
    np_arr = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if frame is None:
        return jsonify({"error": "Failed to decode image."}), 400

    try:
        is_fall = fall_service.detect_fall_from_frame(frame)
    except Exception as e:
        return jsonify({"error": f"Error during fall detection: {str(e)}"}), 500

    result = {"fall_detected": is_fall}

    if is_fall:
        alert_message = "Fall detected! Immediate assistance required."
        notifier.send_telegram_alert(alert_message)
        result["alert_sent"] = True
    else:
        result["alert_sent"] = False

    return jsonify(result)

@app.route("/", methods=["GET"])
def index():
    return "Fall Detection API is running. Use /detect_fall to POST an image for analysis.", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
