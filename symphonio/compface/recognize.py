import pickle

import face_recognition
from PIL import Image
import io
import numpy


def recognize_from_bytes(bytearray: [bytes]):
    image = Image.open(io.BytesIO(bytearray))
    return recognize_image(image)


def recognize_image(pil_image: Image.Image) -> [int]:
    image_encoding = numpy.array(pil_image)
    face_encodings = face_recognition.face_encodings(image_encoding)

    file = open("train_data", "rb")
    train_data = pickle.load(file)
    file.close()

    known_faces = [encoding for (encoding, _) in train_data]
    ids = [composer_id for (_, composer_id) in train_data]

    result = []
    for encoding in face_encodings:
        recognized = face_recognition.compare_faces(known_faces, encoding)
        for i in range(len(recognized)):
            if recognized[i]:
                result.append(ids[i])
                break
    return result
