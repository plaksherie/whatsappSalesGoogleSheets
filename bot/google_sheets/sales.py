import logging
import traceback

from gspread.utils import column_letter_to_index, rowcol_to_a1

from bot.google_sheets.base import BaseSheet
from bot.whatsapp.config import WhatsappMessagesConfig


class SheetSales(BaseSheet):
    def set_google_drive_url_file(
            self,
            find_id: str,
            google_drive_url: str,
            config: WhatsappMessagesConfig
    ) -> None:
        try:
            cell = self.worksheet.find(find_id, in_column=column_letter_to_index(config.column_order_number))
            cell_url_col_index = column_letter_to_index(config.column_for_link_file)
            cell_url = self.worksheet.acell(f'{rowcol_to_a1(row=cell.row, col=cell_url_col_index)}')
            new_value = google_drive_url
            if cell.value != '':
                new_value = f'{cell_url.value}; {new_value}'
            self.worksheet.update_cell(row=cell.row, col=cell_url_col_index,
                                       value=new_value)
            logging.info(f'Проставлена ссылка {google_drive_url} для {find_id}')
        except Exception as e:
            logging.error('Ошибка при вставке url файла в таблицу')
            traceback.print_exc()
