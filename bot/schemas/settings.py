import tomllib
from pathlib import Path

from pydantic import BaseModel


class SeleniumSettings(BaseModel):
    path_profiles: str
    profile_name: str
    user_agent: str
    browser_version: int
    timeout_get_messages: float
    timeout_loading_first_messages: float
    headless: bool


class WhatsappSettings(BaseModel):
    chat_name: str


class GoogleSheetsSettings(BaseModel):
    config_url_sheet: str
    config_worksheet_name: str


class GoogleDriveSettings(BaseModel):
    folder_id_uploads: str


class Settings(BaseModel):
    selenium: SeleniumSettings
    whatsapp: WhatsappSettings
    google_sheets: GoogleSheetsSettings
    google_drive: GoogleDriveSettings

    @staticmethod
    def get(mode: str) -> "Settings":
        return Settings.model_validate(tomllib.loads(Path(f'config.{mode}.toml').read_text(encoding='utf-8')))
