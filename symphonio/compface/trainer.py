import face_recognition
import pickle


def train(composer_connections):
    train_data = []
    for (filename, id) in composer_connections:
        loaded_image = face_recognition.load_image_file(filename)
        encoding = face_recognition.face_encodings(loaded_image)
        train_data.append((encoding[0], id))
    file = open("train_data", "wb")
    pickle.dump(train_data, file)
    file.close()
