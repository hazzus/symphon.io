import pickle

import face_recognition
from PIL import Image
import io
import numpy
from compface.models import ComposerRecognitionData

composers = ComposerRecognitionData.objects.all()
known_faces = []
ids = []
for composer in composers:
    known_faces.append(pickle.loads(composer.data))
    ids.append(composer.composer.id)


def recognize_from_bytes(bytearray: [bytes]):
    image = Image.open(io.BytesIO(bytearray))
    return recognize_image(image)


def recognize_image(pil_image: Image.Image) -> [int]:
    image_encoding = numpy.array(pil_image)
    face_encodings = face_recognition.face_encodings(image_encoding)

    global known_faces
    global ids

    result = []
    for encoding in face_encodings:
        recognized = face_recognition.compare_faces(known_faces, encoding)
        for i in range(len(recognized)):
            if recognized[i]:
                result.append(ids[i])
                break
    return result
