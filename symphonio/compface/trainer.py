import face_recognition
import pickle
from symphonio.compface.models import ComposerRecognitionData


def train(composer_connections):
    train_data = []
    for (filename, id) in composer_connections:
        loaded_image = face_recognition.load_image_file(filename)
        encoding = face_recognition.face_encodings(loaded_image)
        try:
            train_data.append((encoding[0], id))
        except IndexError:
            print("Could not get face from " + filename + " of " + str(id))
    file = open("train_data", "wb")
    pickle.dump(train_data, file)
    file.close()


def add_composer_encoding(id, image):
    """
    Raises FaceNotFound exception
    """
    encoding = face_recognition.face_encodings(image)
    composer = ComposerRecognitionData.objects.create(composer=id, data=encoding)
    ComposerRecognitionData.objects.add()

