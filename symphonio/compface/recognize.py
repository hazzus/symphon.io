import pickle

import face_recognition
from PIL import Image
import io
import numpy
from binascii import a2b_base64
from .models import ComposerRecognitionData

urldataprefix = "data:image/jpeg;base64,"

known_faces = []
ids = []


def recognize_from_bytes(bytearray):
    image = Image.open(io.BytesIO(bytearray))
    return recognize_image(image)


def recognize_image(pil_image):
    """
    :returns array of composer id's
    if there is no faces on image, returns [-1]
    if there is no matches, returns []
    """
    composers = ComposerRecognitionData.objects.all()
    for composer in composers:
        known_faces.append(pickle.loads(composer.data))
        ids.append(composer.composer.id)

    pil_image = pil_image.convert('RGB')
    image_encoding = numpy.array(pil_image)
    face_encodings = face_recognition.face_encodings(image_encoding)
    result = []
    if len(face_encodings) == 0:
        return []
    for encoding in face_encodings:
        recognized = face_recognition.compare_faces(known_faces, encoding)
        for i in range(len(recognized)):
            if recognized[i]:
                result.append(ids[i])
                break
    if len(result) == 0:
        return [-1]
    return result


def recognize_url_image(url_image):
    if not url_image.startswith(urldataprefix):
        print('Unsupported datatype exception')
        return
    binary_data = a2b_base64(url_image[len(urldataprefix):])
    return recognize_from_bytes(binary_data)
