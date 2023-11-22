import cv2
import os

# Function to create a folder if it doesn't exist
def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

# Load the pre-trained face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Reading the video
source = cv2.VideoCapture('ggg.mp4')  # Replace 'input.mp4' with your video file

# We need to set resolutions.
frame_width = int(source.get(3))
frame_height = int(source.get(4))
size = (frame_width, frame_height)

# Create a folder to store extracted faces
faces_folder = 'extracted_faces'
create_folder(faces_folder)

# Create a VideoWriter object for grayscale video
result = cv2.VideoWriter('gray.avi',
                         cv2.VideoWriter_fourcc(*'XVID'),
                         10, size, 0)

# Frame count for naming the extracted faces
frame_count = 0

while True:
    # Extracting frames
    ret, frame = source.read()

    if not ret:
        print("No frame read or end of video.")
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        # Crop the face from the grayscale frame
        face = gray[y:y + h, x:x + w]

        # Save the extracted face as an image in the folder
        cv2.imwrite(f'{faces_folder}/face_{frame_count}.jpg', face)
        frame_count += 1

        # Display the extracted face (optional)
        cv2.imshow("Extracted Face", face)
        cv2.waitKey(100)  # Adjust waitKey time if needed

    # Write the grayscale frame to the output video
    result.write(gray)

    # Display the grayscale video
    cv2.imshow("Grayscale Video", gray)

    # Exiting the loop
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

# Closing windows and releasing resources
cv2.destroyAllWindows()
source.release()
result.release()
