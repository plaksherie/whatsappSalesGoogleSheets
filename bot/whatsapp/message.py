from typing import Optional

from pydantic import BaseModel

from selenium.webdriver.remote.webelement import WebElement

from bot.whatsapp.image import WhatsappImage


class WhatsappMessage(BaseModel):
    id: str
    quote: Optional[WebElement] = None
    text: str
    media: Optional[WhatsappImage] = None

    class Config:
        arbitrary_types_allowed = True
