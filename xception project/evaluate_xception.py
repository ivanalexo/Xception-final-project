import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

model = load_model('./weights/model_xception_v10.h5')

data = '../dataset/'
validation_datagen = ImageDataGenerator(rescale=1./255)
validation_generator = validation_datagen.flow_from_directory(
    data,
    target_size=(256, 256),
    batch_size=16,
    class_mode='binary',
    shuffle=False
)

# Get filenames, true labels, and predicted probabilities
filenames = validation_generator.filenames
y_true = validation_generator.classes
y_pred_prob = model.predict(validation_generator)
y_pred = np.round(y_pred_prob)

# Create a DataFrame
pd.set_option('display.width', 120)
result_df = pd.DataFrame({
    'Filename': filenames,
    'True_Label': y_true,
    'Predicted_Probability': y_pred_prob.flatten(),
    'Predicted_Label': y_pred.flatten()
}).to_csv('./xception_data?v10.csv', sep=',', header=True)

# Display the DataFrame
print(result_df)


# Evaluate the model
evaluation = model.evaluate(validation_generator)
print("Validation Loss:", evaluation[0])
print("Validation Accuracy:", evaluation[1])

# Calculate and print precision
precision = precision_score(y_true, y_pred)
print("Precision:", precision)

# Calculate and print accuracy
accuracy = accuracy_score(y_true, y_pred)
print("Accuracy:", accuracy)
