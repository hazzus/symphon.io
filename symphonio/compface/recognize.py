import face_recognition


def recognize(filename):
    image = face_recognition.load_image_file(filename)
    face_encoding = face_recognition.face_encodings(image)
    saple_image = face_recognition.load_image_file("dicaprio.jpg")
    known_face = [face_recognition.face_encodings(saple_image)]
    result = face_recognition.compare_faces(known_face, face_encoding)
    return result
