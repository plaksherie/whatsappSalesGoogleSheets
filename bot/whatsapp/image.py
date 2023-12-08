from pydantic import BaseModel


class WhatsappImage(BaseModel):
    url: str
