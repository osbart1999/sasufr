import cv2 as cv
import numpy as np
import os
import time
from datetime import *
from PIL import Image
from main_app.models import Test_Attendance, Test_Student, Test_Student_Attendance, Test_Student_Image
from django.conf import settings
import shutil
# import face_recognition





# settings for face recorgnition algorithms
dataset_path = os.path.join(settings.BASE_DIR, 'media/training')
detector_path = os.path.join(settings.BASE_DIR, 'cascades/haarcascade_frontalface_default.xml')
trainer_path = os.path.join(settings.BASE_DIR, 'trainer/trainer.yml')


def face_recognition(test_img):
    grayImg = cv.cvtColor(test_img, cv.COLOR_BGR2GRAY)
    face_haar_cascade = cv.CascadeClassifier(detector_path)
    faces = face_haar_cascade.detectMultiScale(grayImg, scaleFactor=1.40, minNeighbors=5)
    return faces, grayImg


def train_recorgniser():
    path = dataset_path
    detector = cv.CascadeClassifier(detector_path)

    recorgniser = cv.face.LBPHFaceRecognizer_create()

    # get image data and respective labels
    def getImageData(path):
        images = [os.path.join(path,f) for f in os.listdir(path)]
        samples = []
        ids = []

        for imge in images:
            pillow_image = Image.open(imge).convert('L') #Grayscale image for opencv2
            # pillow_image = Image.open
            numpy_image = np.array(pillow_image, 'uint8')
            id = int(os.path.split(imge)[-1].split(".")[1])
            det_faces = detector.detectMultiScale(numpy_image)

            for (x,y,w,h) in det_faces:
                samples.append(numpy_image[y:y+h, x:x+w])
                ids.append(id)

        return samples,ids

    print('Training recorgniser on the input faces....')
    all_faces,ids = getImageData(path)
    recorgniser.train(all_faces, np.array(ids))

    # save trainer file
    recorgniser.write(trainer_path) 

    # print(f'Trained {0}% faces, exiting the program....'.format(len(np.unique(ids))))

    return f'Training completed...'




def analyse_faces(video, attendance_id):

    # initialise detector and trainer files
    detector = cv.CascadeClassifier(detector_path)
    recorgniser = cv.face.LBPHFaceRecognizer_create()
    recorgniser.read(trainer_path)

    
    # get current attendance
    cur_attendance = Test_Attendance.objects.get(id=attendance_id)

    # get students from db
    students = Test_Student.objects.all()
    print('Students', students)
    ids = []

    for student in students:
        ids.append(student.id)
    
    print('ids...', ids)
        # print(student)


    # Extract Images from  a video
    cap = cv.VideoCapture('/home/jimson/Desktop/new.mp4')
    minWin = 0.1*cap.get(3) 
    minHei = 0.1*cap.get(3) 

    print('video..', cap)

    face_locations = []

    while True:
        # Grab a single frame of video
        ret, frame = cap.read()    # Convert the image from BGR color (which OpenCV uses) to RGB   
        # color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]    # Find all the faces in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)    

        print('faces,', face_locations)

        for top, right, bottom, left in face_locations:
            # Draw a box around the face
            cv.rectangle(frame, (left, top), (right, bottom), (0, 0,  
            255), 2)
                # Display the resulting image
        # cv.imshow('Video', frame)
        

        # # Wait for Enter key to stop
        # if cv.waitKey(25) == 13:
        #     break

    # while True:
    #     ret, frame = cap.read()
    #     gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #     # faces = face_recognition(frame)


    #     faces = detector.detectMultiScale(
    #         gray,
    #         scaleFactor = 1.2,
    #         minNeighbors = 5,
    #         minSize = (int(minWin), int(minHei)),
    #     )
    #     print('faces..', faces)


    #     for (x,y,h,w) in faces:
    #         cv.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 4)
    #         print('intialising faces....')
    #         print('face', (x,y,h,w))
    #         id = 0
    #         for id in ids:
    #             print(id)

    #             id, confidence = recorgniser.predict(frame[y:y+h,x:x+w]) #.......

    #             print('confidence...', confidence)

    #             if confidence < 100 > 40:
    #                 # id = students_names[id]
    #                 confidence = "{0}%".format(round(100 - confidence))
    #                 # create student attendance object here
    #                 cur_student = Test_Student.objects.get(id=id)
    #                 Test_Student_Attendance.objects.create(student=cur_student, attendance=cur_attendance)
    #                 print(cur_student)

    #             else:
    #                 id = "Unknown"
    #                 confidence = " {0}%".format(round(100 - confidence))
    #                 print('No student ')
    #                 # create a message here 

            
    #         cv.imshow('camera', frame)
    #         k = cv.waitKey(10) & 0xFF
        
    #     if k == 27:
    #         break
    # cap.release()
    # cv.destroyAllWindows()

    return 'Done'


