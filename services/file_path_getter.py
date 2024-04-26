from django.core.files.storage import FileSystemStorage
from YUTA.settings import MEDIA_ROOT
from transliterate import slugify
import re


def get_file_path(file_name, save_path):
    fs = FileSystemStorage()
    file_names = fs.listdir(path=f'{MEDIA_ROOT}/{save_path}')[1]
    extension = file_name[file_name.rfind('.') + 1:]
    slug = slugify(file_name.replace(f'.{extension}', ''), language_code='ru')
    file_name = f'{slug}.{extension}'
    if file_name not in file_names:
        return f'{save_path}/{file_name}'
    else:
        pattern = f'{slug}-\\d+\\.{extension}'
        same_file_names = [file_name for file_name in file_names if re.fullmatch(pattern, file_name)]
        if not same_file_names:
            return f'{save_path}/{slug}-1.{extension}'
        versions = [
            int(file_name.replace(f'{slug}-', '').replace(f'.{extension}', ''))
            for file_name in same_file_names
        ]
        return f'{save_path}/{slug}-{max(versions) + 1}.{extension}'
