import cv2
import face_recognition
import os

video_dir = './Celeb-DF-2/'

output_dir = 'MesoNet/fake_images_v2/'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for video_file in os.listdir(video_dir):
    video = cv2.VideoCapture(os.path.join(video_dir, video_file))

    frame_counter = 0
    while video.isOpened():
        ret, frame = video.read()

        if not ret:
            break
        frame_counter += 1

        if frame_counter % 30 == 0:
            face_locations = face_recognition.face_locations(frame)

            for i, face_locations in enumerate(face_locations):
                top, right, bottom, left = face_locations
                face_image = frame[top:bottom, left:right]

                cv2.imwrite(os.path.join(output_dir,
                f'{video_file}_frame{frame_counter}_face{i}.jpg'), face_image)
    video.release()