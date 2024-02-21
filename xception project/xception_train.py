import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import Xception
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, BatchNormalization, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import classification_report
from tensorflow.keras.utils import plot_model
from tensorflow.keras.callbacks import EarlyStopping
from pipeline import *
import pandas as pd
import matplotlib.pyplot as plt

# Replace for your dataset directory
data_dir = '../dataset/'
img_width, img_height = 224, 224
batch_size = 16
epochs = 6

datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.1
)

train_generator = datagen.flow_from_directory(
    data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary',
    subset='training',
    shuffle=True
)

validation_generator = datagen.flow_from_directory(
    data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary',
    subset='validation',  # Specify validation set
    shuffle=False
)

base_model = Xception(weights=None, include_top=False, input_shape=(img_width, img_height, 3))
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128)(x)
x = BatchNormalization()(x)
x = tf.keras.activations.relu(x)
x = Dropout(0.5)(x)
predictions = Dense(1, activation='sigmoid')(x)
model = Model(inputs=base_model.input, outputs=predictions)

model.compile(optimizer=Adam(lr=1e-4), loss='binary_crossentropy', metrics=['accuracy'])

early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
hist = model.fit(train_generator, epochs=epochs, validation_data=validation_generator, callbacks=[early_stopping])

model.save('weights/model_xception.h5')

test_generator = datagen.flow_from_directory(
    data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary',
    subset='validation'  # Use the validation set for evaluation
)
filenames = test_generator.filenames
y_true = test_generator.classes
y_pred_prob = model.predict(test_generator)
y_pred = (y_pred_prob > 0.5).astype(int)

pd.set_option('display.width', 120)
result_df = pd.DataFrame({
    'Filename': filenames,
    'True_Label': y_true,
    'Predicted_Probability': y_pred_prob.flatten(),
    'Predicted_Label': y_pred.flatten()
}).to_csv('./xception_data3.csv', sep=',', header=True)

# Print classification report
report = classification_report(y_true, y_pred, target_names=['Real', 'Deepfake'])
print(report)
plot_history_loss(hist)
plot_history_acc(hist)

# Save the model diagram
plot_model(model, to_file='./model_diagram6.png', show_shapes=True)