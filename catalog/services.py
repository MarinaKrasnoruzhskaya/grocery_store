import base64
import io
import os
from io import BytesIO

import magic
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

from config.settings import BASE_DIR


def get_test_file(name):
    """ Возвращает загруженный файл """

    image_path = os.path.join(BASE_DIR, "catalog", "image", "data", name)
    # mime = magic.Magic(mime=True)
    # content_type = mime.from_file(image_path)
    # tmp_file = SimpleUploadedFile(image_path, "file_content", content_type=content_type)
    # return tmp_file

    # with open(image_path, 'rb') as image_file:
    #     base64_bytes = base64.b64encode(image_file.read())
    #     print(base64_bytes)
    #
    #     base64_string = base64_bytes.decode()
    #     print(base64_string)
    #
    #     im = Image.open(BytesIO(base64.b64decode(base64_bytes)))
    #     print(im)
    #
    # return im
    byte_io = io.BytesIO()
    with open(image_path, 'rb') as file:
        byte_io.write(file.read())
        byte_io.seek(0)

    mime = magic.Magic(mime=True)
    content_type = mime.from_file(image_path)

    return InMemoryUploadedFile(
        file=byte_io,
        field_name='image',
        name=name,
        content_type=content_type,
        size=os.path.getsize(image_path),
        charset=None
    )

