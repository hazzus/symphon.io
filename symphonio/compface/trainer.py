from .models import ComposerRecognitionData, Composer, get_photo_encoding
from .recognize import known_faces, ids


def add_composer_encoding(id, image):
    """
    Raises FaceNotFound exception
    """
    try:
        encoding = get_photo_encoding(image)
    except IndexError:
        print("Could not find any face")
        return
    composer = Composer.objects.get(pk=id)
    composer_encoded = ComposerRecognitionData.objects.create(composer=composer, data=encoding)
    composer_encoded.save()
    known_faces.append(encoding)
    ids.append(id)
