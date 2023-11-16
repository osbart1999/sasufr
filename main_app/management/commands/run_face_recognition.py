import argparse
from django.core.management.base import BaseCommand
from django.conf import settings
from subprocess import run
from pathlib import Path

from main_app.detector import encode_known_faces, recognize_faces, validate

class Command(BaseCommand):
    help = 'Run face recognition tasks'

    def add_arguments(self, parser):
        parser.add_argument("--train", action="store_true", help="Train on input data")
        parser.add_argument("--validate", action="store_true", help="Validate trained model")
        parser.add_argument("--test", action="store_true", help="Test the model with an unknown image")
        parser.add_argument("-m", action="store", default="hog", choices=["hog", "cnn"], help="Which model to use for training: hog (CPU), cnn (GPU)")
        parser.add_argument("-f", action="store", help="Path to an image with an unknown face")

    def handle(self, *args, **options):
        train = options.get("train")
        validate = options.get("validate")
        test = options.get("test")
        model = options.get("m")
        image_path = options.get("f")

        encodings_location = Path(settings.MEDIA_ROOT) / 'output' / 'encodings.pkl'

        if train:
            encode_known_faces(model=model, encodings_location=encodings_location)

        if validate:
            validate(model=model)

        if test and image_path:
            recognize_faces(image_location=image_path, model=model)

