import cv2 as cv
import numpy as np
import os
import time
from datetime import *
from PIL import Image
from main_app.models import Attendance, Student, StudentAttendance, StudentFaceImage
from django.conf import settings
import shutil
# import face_recognition



# settings for face recorgnition algorithms
dataset_path = os.path.join(settings.BASE_DIR, 'media/training')
detector_path = os.path.join(settings.BASE_DIR, 'cascades/haarcascade_frontalface_default.xml')
trainer_path = os.path.join(settings.BASE_DIR, 'trainer/trainer.yml')

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
