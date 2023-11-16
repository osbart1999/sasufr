import os
import pickle
import cv2
import dlib
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
#from .student_views import create_folder_for_user
from .student_views import create_folder_for_user
import pandas as pd
from datetime import datetime
from imutils import paths
import numpy as np
from .models import*

# Define the shape_to_np function
def shape_to_np(shape, student_instance, dtype="int"):
    coords = np.zeros((shape.num_parts, 2), dtype=dtype)
    for i in range(0, shape.num_parts):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    email = student_instance.admin.email  # Access the email through the Student model
    return coords, email

# Paths
input_folder = "student_capture_faces"
output_folder = "trained_images"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_ROOT = os.path.join(BASE_DIR, output_folder)
shape_predictor_path = os.path.join(MEDIA_ROOT, 'shape_predictor_68_face_landmarks.dat')

# Load face detector and shape predictor from dlib
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(shape_predictor_path)

# Iterate through student folders
for student_folder in os.listdir(input_folder):
    student = Student.objects.get(admin__email=student_folder)  # Get the student instance
    student_input_folder = os.path.join(input_folder, student_folder)

    # Process images and save trained faces
    for image_path in paths.list_images(student_input_folder):
        # Load the image
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = detector(gray)

        # Process each detected face
        for face in faces:
            # Get facial landmarks and student instance
            shape = predictor(gray, face)
            face_descriptor, _ = shape_to_np(shape, student)

            # Save the facial landmarks in the database
            captured_face = CapturedFaceImage(student=student, face_image=image_path)
            captured_face.save()

            # Save the trained image
            output_path = os.path.join(output_folder, f"trained_{os.path.basename(image_path)}")
            cv2.imwrite(output_path, image)

print("Training completed, images stored in the trained_images folder, and facial landmarks stored in the database.")

def handle_upload_attendance_file(attendance_file, file_type):
    media_root = 'media/'
    
    if file_type == 'video':
        video_path = os.path.join(media_root, 'attendance_files', 'videos', attendance_file.name)
        with open(video_path, 'wb+') as destination:
            for chunk in attendance_file.chunks():
                destination.write(chunk)
        
        # Call function to extract faces from video
        captured_faces_path = extract_faces_from_video_or_group_image(video_path)
        return JsonResponse({'status': 'success', 'message': 'Faces extracted successfully.', 'faces_path': captured_faces_path})

    elif file_type == 'photos':
        image_path = os.path.join(media_root, 'attendance_files', 'images', attendance_file.name)
        with open(image_path, 'wb+') as destination:
            for chunk in attendance_file.chunks():
                destination.write(chunk)
        
        # Call function to extract faces from image
        captured_faces_path = extract_faces_from_video_or_group_image(image_path)
        return JsonResponse({'status': 'success', 'message': 'Faces extracted successfully.', 'faces_path': captured_faces_path})

    else:
        # Invalid file type
        return JsonResponse({'status': 'error', 'message': 'Invalid file type.'})
            
"""def handle_upload_attendance_file(request):
    media_root = 'media/'
    attendance_file = request.FILES['attendance_file']
    file_type = request.POST.get('file_type')

    if file_type == 'video':
        # Handle video file upload
        video_path = os.path.join(media_root, 'attendance_files', 'videos', attendance_file.name)
        with open(video_path, 'wb+') as destination:
            for chunk in attendance_file.chunks():
                destination.write(chunk)
        
        # Call function to extract faces from video
        captured_faces_path = extract_faces_from_video_or_group_image(video_path)
        return JsonResponse({'status': 'success', 'message': 'Faces extracted successfully.', 'faces_path': captured_faces_path})

    elif file_type == 'photos':
        # Handle image file upload
        image_path = os.path.join(media_root, 'attendance_files', 'images', attendance_file.name)
        with open(image_path, 'wb+') as destination:
            for chunk in attendance_file.chunks():
                destination.write(chunk)
        
        # Call function to extract faces from image
        captured_faces_path = extract_faces_from_video_or_group_image(image_path)
        return JsonResponse({'status': 'success', 'message': 'Faces extracted successfully.', 'faces_path': captured_faces_path})

    else:
        # Invalid file type
        return JsonResponse({'status': 'error', 'message': 'Invalid file type.'})
        """



def extract_faces_from_video_or_group_image(file_path):
    # Determine file type based on extension
    file_extension = os.path.splitext(file_path)[1].lower()

    # Code to extract frames from video
    if file_extension in ['.mp4', '.avi', '.mov']:  # Assuming common video formats
        # Open the video file
        cap = cv2.VideoCapture(file_path)
        face_detector = dlib.get_frontal_face_detector()
        captured_faces_path = 'media/captured_faces'
        os.makedirs(captured_faces_path, exist_ok=True)
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detector(gray)

            for face in faces:
                x, y, w, h = face.left(), face.top(), face.width(), face.height()
                face_region = frame[y:y+h, x:x+w]
                face_path = os.path.join(captured_faces_path, f"frame_{frame_count}.jpg")
                cv2.imwrite(face_path, face_region)
                frame_count += 1

        cap.release()
        return captured_faces_path

    # Code to extract frames from group images
    elif file_extension in ['.jpg', '.jpeg', '.png']:  # Assuming common image formats
        # Create a temporary video file from the images
        temp_video_path = 'media/temp_video.mp4'
        frame_images = [os.path.join(file_path, img) for img in sorted(os.listdir(file_path))]
        frame_size = cv2.imread(frame_images[0]).shape[1], cv2.imread(frame_images[0]).shape[0]
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Video codec for MP4 format
        out = cv2.VideoWriter(temp_video_path, fourcc, 20.0, frame_size)

        for img_path in frame_images:
            img = cv2.imread(img_path)
            out.write(img)

        out.release()

        # Extract frames from the temporary video file
        captured_faces_path = extract_faces_from_video_or_group_image(temp_video_path)
        
        # Delete the temporary video file
        os.remove(temp_video_path)

        return captured_faces_path

    else:
        # Invalid file type
        return None

def compare_faces_with_trained_images(captured_faces_path):
    # Code to compare faces in captured_faces with those in trained_images
    descriptors = []
    student_emails = []

    # Load trained descriptors and corresponding student emails
    for descriptor_file in os.listdir('trained_images'):
        if descriptor_file.endswith('_descriptors.pkl'):
            student_email = descriptor_file.replace('_descriptors.pkl', '')
            student_emails.append(student_email)
            with open(os.path.join('trained_images', descriptor_file), 'rb') as f:
                descriptors.append(pickle.load(f))

    # Initialize Dlib face detector and recognition model
    detector = dlib.get_frontal_face_detector()
    face_recognition_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

    # Initialize attendance data
    attendance_data = {email: 0 for email in student_emails}
    
    for face_file in os.listdir(captured_faces_path):
        face_path = os.path.join(captured_faces_path, face_file)
        frame = cv2.imread(face_path)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            shape = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")(frame, face)
            face_descriptor = face_recognition_model.compute_face_descriptor(frame, shape)

            # Compare the face descriptor with known descriptors
            for i, known_descriptors in enumerate(descriptors):
                for known_descriptor in known_descriptors:
                    # You can set an appropriate threshold for face recognition similarity
                    similarity = dlib.face_recognition_model_v1.compute_face_descriptor_similarity(face_descriptor, known_descriptor)
                    if similarity > 0.6:
                        recognized_student = student_emails[i]
                        # Update attendance data
                        attendance_data[recognized_student] += 1

    return attendance_data

def create_attendance_folder(session, course, subject, student_emails):
    # Code to create a folder in the attendance folder with session, course, subject,
    # student emails, date, and time
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H-%M-%S")
    email_list = '_'.join(student_emails)
    folder_name = f"{session}_{course}_{subject}_{email_list}_{current_date}_{current_time}"
    attendance_folder = os.path.join('attendance', folder_name)
    os.makedirs(attendance_folder, exist_ok=True)
    return attendance_folder

def save_attendance_to_excel(attendance_data, folder_path, student_info, absent_students):
    # Code to save attendance data to an Excel file inside the specified folder
    excel_file_path = os.path.join(folder_path, 'attendance.xlsx')
    
    # Prepare data for the Excel file
    present_records = []
    for email, status in attendance_data.items():
        full_name = student_info.get(email, {}).get('full_name', 'Unknown Student')
        if status > 0:
            present_records.append({'Full Name': full_name, 'Email': email, 'Attendance Status': 'Present'})

    absent_records = []
    for email in absent_students:
        full_name = student_info.get(email, {}).get('full_name', 'Unknown Student')
        absent_records.append({'Full Name': full_name, 'Email': email, 'Attendance Status': 'Absent'})

    # Combine present and absent records
    attendance_records = present_records + absent_records
    
    # Create a DataFrame and save to Excel
    df = pd.DataFrame(attendance_records)
    df.to_excel(excel_file_path, index=False)