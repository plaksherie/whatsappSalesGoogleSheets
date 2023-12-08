from typing import Optional

from pydantic import BaseModel


class WhatsappMessagesConfig(BaseModel):
    comment: Optional[str]
    short_phrase: Optional[str]
    link_sales_sheet: Optional[str]
    name_worksheet: Optional[str]
    column_for_link_file: Optional[str]
    column_order_number: Optional[str]
