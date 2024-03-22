import uuid
from django.utils.deconstruct import deconstructible

@deconstructible
class UniqueFilenameGenerator:
    def __init__(self, sub_path):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        return f"{self.sub_path}/{unique_filename}"