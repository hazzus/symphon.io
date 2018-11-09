import face_recognition
import PIL.Image as Image
import io
import numpy


def recognize(bytes):
    image = Image.open(io.BytesIO(bytes))
    imagearr = numpy.asarray(image)
    face_encodings = face_recognition.face_encodings(imagearr)
    sample_image = face_recognition.load_image_file("img/dicaprio.jpg")

    known_faces = face_recognition.face_encodings(sample_image)
    result = []
    for encoding in face_encodings:
        recognized = face_recognition.compare_faces(known_faces, encoding)
        for match in recognized:
            if match:
                result.append("kek")
    return result
