from typing import List

import gspread

from bot.google_sheets.base import BaseSheet
from bot.whatsapp.config import WhatsappMessagesConfig


class SheetConfig(BaseSheet):
    def get_whatsapp_configs(
            self,
    ) -> List[WhatsappMessagesConfig]:
        configs = []
        list_of_lists = self.worksheet.get_values("A:F")
        for i, row in enumerate(list_of_lists):
            if i == 0:
                continue
            configs.append(WhatsappMessagesConfig(
                comment=row[0],
                short_phrase=row[1],
                link_sales_sheet=row[2],
                name_worksheet=row[3],
                column_order_number=row[4],
                column_for_link_file=row[5],
            ))
        return configs
