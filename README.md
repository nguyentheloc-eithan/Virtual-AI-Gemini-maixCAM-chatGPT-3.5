
# Virtual-AI-Gemini-maixCAM-chatGPT-3.5 Documentation

Welcome to the **Virtual-AI-Gemini-maixCAM-chatGPT-3.5** project – a cutting-edge, modular system designed for real-time fall detection with integrated intelligent virtual assistant support. This project leverages advanced machine learning, computer vision, and conversational AI to deliver a robust solution for monitoring and alerting in environments where fall detection is critical.

----------

## Project Overview

**Virtual-AI-Gemini-maixCAM-chatGPT-3.5** is built to:

-   **Capture Video Streams:** Utilize maixCAM (or any compatible camera) for real-time video feed.
-   **Detect Falls:** Analyze video frames using a TensorFlow-based ML model to determine if a fall has occurred.
-   **Notify Stakeholders:** Send immediate alerts via Telegram when a fall is detected.
-   **Engage a Virtual Assistant:** Use the ChatGPT API to offer intelligent insights, context-aware support, and conversation-based troubleshooting through a virtual assistant.

----------

## Architecture and Modules

The project is designed in a modular fashion to promote maintainability and extensibility. Each service or module is responsible for a specific aspect of the overall system.

### 1. **Camera Service**

-   **File:** `services/maxcam_service.py`
-   **Purpose:**  
    Provides an interface for capturing video frames from the maixCAM device. It handles camera initialization, setting the desired resolution, frame acquisition, and proper resource cleanup.
-   **Key Features:**
    -   Connection with maixCAM hardware.
    -   Frame display for debugging and visual feedback.
    -   Easy integration with downstream services.

### 2. **Fall Detection Service**

-   **File:** `fall_service.py`
-   **Purpose:**  
    Implements an ML-based approach for fall detection. The service loads a pre-trained TensorFlow model, preprocesses the captured frames, and runs inference to determine whether a fall has occurred.
-   **Key Features:**
    -   Model loading and error handling.
    -   Frame preprocessing (resizing, normalization, etc.).
    -   Inference logic with a configurable probability threshold.
    -   Real-time performance for continuous video stream analysis.

### 3. **Notification Service**

-   **File:** `notification_service.py`
-   **Purpose:**  
    Sends alert notifications via the Telegram Bot API when a fall is detected. This allows for immediate human intervention or further automated processes.
-   **Key Features:**
    -   Integration with Telegram using secure API calls.
    -   Flexible configuration for Telegram Bot Token and Chat ID.
    -   Logging of successful and failed notification attempts.

### 4. **GPT Service**

-   **File:** `gpt_service.py`
-   **Purpose:**  
    Acts as a fully smart virtual assistant by interfacing with the ChatGPT API. This service maintains conversation context, allowing for multi-turn dialogue and providing intelligent responses based on user prompts.
-   **Key Features:**
    -   Conversation context management to provide contextual and coherent responses.
    -   Retry logic to handle API failures gracefully.
    -   Detailed logging for debugging and operational transparency.
    -   Customizable system prompt to define the assistant's persona.

### 5. **REST API Service**

-   **File:** `main.py`
-   **Purpose:**  
    Exposes a REST API using Flask, allowing clients to send images for fall detection and triggering appropriate responses. The API integrates fall detection, notification, and optionally the virtual assistant functionalities.
-   **Key Features:**
    -   Endpoint `/detect_fall` for processing uploaded images.
    -   JSON responses indicating fall detection results and alert status.
    -   Seamless integration with the other modules (Fall Detection and Notification).

----------

## How It Works

1.  **Video Capture:**  
    The system initializes the maixCAM through the Camera Service. It continuously captures video frames, which are forwarded to the Fall Detection Service.
    
2.  **Fall Detection:**  
    Each frame is preprocessed (resized, normalized, etc.) and passed to the ML model in the Fall Detection Service. If the model determines that the fall probability exceeds a preset threshold, a fall event is triggered.
    
3.  **Notification:**  
    On detecting a fall, the Notification Service sends an immediate alert message to a pre-configured Telegram chat. This ensures that responsible parties are notified in real-time.
    
4.  **Virtual Assistant Interaction:**  
    The GPT Service, acting as a virtual assistant, can engage in multi-turn conversations to help interpret the event, offer troubleshooting advice, or provide further guidance. The conversation context is maintained across interactions to offer a “smart” and personalized experience.
    
5.  **API Exposure:**  
    The REST API, exposed via Flask in `main.py`, provides an interface for external systems to interact with the fall detection engine. Clients can send images, receive analysis results, and trigger notifications.
