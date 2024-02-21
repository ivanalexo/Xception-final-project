import face_recognition
import os
import cv2

def extract_faces(image_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(image_dir):
        image_path = os.path.join(image_dir, filename)
        image = cv2.imread(image_path)
        #rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(image)
        for face_location in face_locations:
            top, right, bottom, left = face_location

            face_image = image[top:bottom, left:right]
            output_filename = os.path.join(output_dir, filename[:-4] + "_face.jpg")
            cv2.imwrite(output_filename, face_image)

if __name__ == "__main__":
    image_dir = "./real people/lfw/Robert_Downey_Jr"
    output_dir = "./dataset2/"

    extract_faces(image_dir, output_dir)