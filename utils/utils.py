import os
from werkzeug.utils import secure_filename

def save_uploaded_file(file_data, upload_folder):
    if not file_data or (isinstance(file_data, str) and not file_data.strip()):
        return None

    if hasattr(file_data, 'filename'):
        if file_data.filename == '':
            return None
        filename = secure_filename(file_data.filename)

        try:
            os.makedirs(upload_folder, exist_ok=True)
        except PermissionError:
            raise Exception(f"Нет прав на создание папки: {upload_folder}")

        full_path = os.path.join(upload_folder, filename)

        try:
            file_data.save(full_path)
            return filename
        except (IOError, OSError) as e:
            raise Exception(f"Не удалось сохранить файл: {e}")
    return file_data
