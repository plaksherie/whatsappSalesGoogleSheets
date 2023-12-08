import logging
import traceback

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.files import GoogleDriveFile


class GoogleDriveUpload:
    def __init__(
            self,
            service_file: str = 'service_account.json'
    ) -> None:
        settings = {
            "client_config_backend": "service",
            "service_config": {
                "client_json_file_path": service_file,
            }
        }
        gauth = GoogleAuth(settings=settings)
        gauth.ServiceAuth()
        self.gauth = gauth
        self.drive = GoogleDrive(gauth)

    def upload_file(
            self,
            folder_id: str,
            file_path: str,
            file_name: str,
            mime_type: str = 'image/jpeg'
    ) -> GoogleDriveFile | None:
        metadata = {
            'parents': [
                {"id": folder_id}
            ],
            'title': file_name,
            'mimeType': mime_type
        }
        file = self.drive.CreateFile(metadata=metadata)
        try:
            file.SetContentFile(file_path)
            file.Upload()
            logging.info(f'Загружен файл {file["title"]} - {file["mimeType"]}')
            return file
        except (Exception,):
            logging.error('Ошибка при загрузке файла в Google Drive')
            traceback.print_exc()
            return None
        finally:
            file.content.close()

