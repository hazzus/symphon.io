import pickle

import face_recognition
from PIL import Image
import io
import numpy
from binascii import a2b_base64

urldataprefix = "data:image/jpeg;base64,"

known_faces = []
ids = []


def recognize_from_bytes(bytearray: [bytes]):
    image = Image.open(io.BytesIO(bytearray))
    return recognize_image(image)


def recognize_image(pil_image: Image.Image) -> [int]:
    image_encoding = numpy.array(pil_image)
    face_encodings = face_recognition.face_encodings(image_encoding)
    result = []
    for encoding in face_encodings:
        recognized = face_recognition.compare_faces(known_faces, encoding)
        for i in range(len(recognized)):
            if recognized[i]:
                result.append(ids[i])
                print("Success!" + str(ids[i]))
                break
    return result


def recognize_url_image(url_image: str) -> [int]:
    if not url_image.startswith(urldataprefix):
        print('Unsupported datatype exception')
        return
    binary_data = a2b_base64(url_image[len(urldataprefix):])
    return recognize_from_bytes(binary_data)
