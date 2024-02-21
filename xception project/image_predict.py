from keras.preprocessing import image
import numpy as np
from keras.models import load_model
import cv2

model = load_model('weights/model_xception_v5.h5')

img_path = ''
img = image.load_img(img_path, target_size=(256, 256))
img_s = cv2.imread(img_path)
height, width, _ = img_s.shape
print("Image size:", height, "x", width)
print("Keras image size:", img.size)
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0) / 255.0

prediction = model.predict(img_array)
print('The probability of the image to being real is {:.2f}%'.format(prediction[0][0] * 100))


if prediction[0][0] > 0.5:
    print('Prediction: Real')
else:
    print('Prediction: Deepfake')
cv2.imshow('Result', img_s)
cv2.waitKey(0)
cv2.destroyAllWindows()