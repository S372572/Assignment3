from flask import Flask, jsonify, request
import numpy as np
import tensorflow as tf
from PIL import Image

app = Flask(__name__)

# Load your TensorFlow model here
model_path = "/Users/abdullah/Desktop/Tkinter Application/tensorflow_env/assets/mobilenet_v1_1.0_224.tflite"
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# Home route
@app.route('/')
def home():
    return "Welcome to the Image Classifier API!"

# Classify route
@app.route('/classify', methods=['POST'])
def classify_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    image = Image.open(image_file).resize((224, 224))
    input_data = np.array(image, dtype=np.uint8)
    input_data = np.expand_dims(input_data, axis=0)

    # Get input and output details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Set tensor
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # Get output tensor
    output_data = interpreter.get_tensor(output_details[0]['index'])
    top_k_indices = output_data[0].argsort()[-5:][::-1]

    # Return the results
    results = [{"label": str(i), "confidence": float(output_data[0][i])} for i in top_k_indices]
    return jsonify(results)

# Handle favicon requests
@app.route('/favicon.ico')
def favicon():
    return "", 204  # No content response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)  # Ensure the correct port is specified
