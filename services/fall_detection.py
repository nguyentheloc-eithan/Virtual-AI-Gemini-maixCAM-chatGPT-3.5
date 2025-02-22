import tensorflow as tf
import numpy as np
import cv2

class FallService:
    def __init__(self, model_path: str, input_size: tuple = (224, 224), threshold: float = 0.5):
        """
        Initializes the FallService by loading the TensorFlow model.
        :param model_path: Path to the TensorFlow model (SavedModel format or .h5 file).
        :param input_size: Expected input image size (width, height).
        :param threshold: Threshold for determining a fall.
        """
        self.input_size = input_size
        self.threshold = threshold
        self.model = self.load_model(model_path)
        print("Fall detection model loaded successfully.")

    def load_model(self, model_path: str):
        """
        Loads the TensorFlow model.
        :param model_path: Path to the model.
        :return: Loaded TensorFlow model.
        """
        try:
            model = tf.keras.models.load_model(model_path)
            return model
        except Exception as e:
            print(f"Error loading model: {e}")
            raise

    def preprocess_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Preprocesses a frame for model input:
          - Resize the frame to input_size.
          - Normalize pixel values to [0, 1].
        :param frame: Input frame (BGR format as from OpenCV).
        :return: Preprocessed frame ready for prediction.
        """
        # Resize the image
        resized_frame = cv2.resize(frame, self.input_size)
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
        # Normalize pixel values
        normalized_frame = rgb_frame.astype('float32') / 255.0
        # Expand dims to create batch of size 1
        input_tensor = np.expand_dims(normalized_frame, axis=0)
        return input_tensor

    def detect_fall_from_frame(self, frame: np.ndarray) -> bool:
        """
        Runs fall detection on the provided frame.
        :param frame: Input frame (BGR format).
        :return: True if a fall is detected, False otherwise.
        """
        input_tensor = self.preprocess_frame(frame)
        # Run inference
        prediction = self.model.predict(input_tensor)
        # For binary classification, we assume:
        # prediction[0][0] = probability of no fall, prediction[0][1] = probability of fall.
        fall_probability = prediction[0][1] if prediction.shape[-1] > 1 else prediction[0][0]
        print(f"Fall probability: {fall_probability:.4f}")
        return fall_probability > self.threshold
