import cv2
import face_recognition
import numpy as np
import base64
import io
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from tensorflow.keras.models import load_model
from PIL import Image

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

model = load_model('../MesoNet/weights/model_xception_v10.h5')

@app.route('/')
@cross_origin()
def hello_world():
    return "Deep Fake Backend"

@app.route('/predict', methods=['POST'])
@cross_origin()
def get_prediction():
    # Get the Base64 encoded image from the request
    base64_image = request.json['image']
    base64_image = base64_image.split(',')[1]

    # Decode the Base64 string to bytes
    image_bytes = base64.b64decode(base64_image)

    # Convert bytes to PIL image
    pil_image = Image.open(io.BytesIO(image_bytes))

    # Convert image to RGB if not already in RGB format
    if pil_image.mode != 'RGB':
        pil_image = pil_image.convert('RGB')

    # Convert PIL image to numpy array
    img_array = np.array(pil_image)

    # Perform face detection
    face_locations = face_recognition.face_locations(img_array)
    print("Detected face locations:", face_locations)
    predictions = []

    # Process each detected face
    for face_location in face_locations:
        top, right, bottom, left = face_location
        face_image = img_array[top:bottom, left:right]
        face_image = cv2.resize(face_image, (224, 224))
        face_image = np.expand_dims(face_image, axis=0) / 255.0

        # Make prediction
        prediction = model.predict(face_image)
        predicted_label = 'Real' if prediction[0][0] > 0.5 else 'Fake'
        color = (0, 255, 0) if prediction[0][0] > 0.5 else (255, 0, 0)
        predictions.append(str(prediction[0][0]))

        # Draw rectangle around the face and put label
        cv2.rectangle(img_array, (left, top), (right, bottom), color, 3)
        cv2.putText(img_array, predicted_label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    # Encode the modified image to Base64 using OpenCV
    rgb_image = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
    _, img_encoded = cv2.imencode('.jpg', rgb_image)
    img_base64 = base64.b64encode(img_encoded).decode('utf-8')

    # Prepare response
    response = {
        'num_faces': len(face_locations),
        'predictions': predictions,
        'image': img_base64
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
