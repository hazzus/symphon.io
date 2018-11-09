import face_recognition
from compface.models import ComposerRecognitionData, Composer
from compface.recognize import known_faces, ids
import pickle
import numpy


def add_composer_encoding(id, image):
    """
    Raises FaceNotFound exception
    """
    image = numpy.array(image)
    try:
        encoding = face_recognition.face_encodings(image)[0]
    except IndexError:
        print("Could not find any face")
        return
    composer = Composer.objects.get(pk=id)
    composer_encoded = ComposerRecognitionData.objects.create(composer=composer, data=pickle.dumps(encoding))
    composer_encoded.save()
    known_faces.append(encoding)
    ids.append(composer.id)
