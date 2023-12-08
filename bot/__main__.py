import logging
import os
import time
import traceback

from bot.config import settings
from bot.google_drive.upload import GoogleDriveUpload
from bot.google_sheets.config import SheetConfig
from bot.google_sheets.sales import SheetSales
from bot.loader import get_driver, checked_message_ids
from bot.whatsapp.whatsapp import Whatsapp


def main():
    driver = get_driver()
    wh = Whatsapp(driver)
    try:
        enter = wh.enter_site()
        driver.save_screenshot('screens/before.png')
        if not enter:
            logging.error('Нужна авторизация для этого профиля браузера')
            input()
        wh.enter_to_chat(settings.whatsapp.chat_name)
        time.sleep(2)
        driver.save_screenshot('screens/enter_chat.png')
        messages = wh.get_new_messages(only_quote=False)
        checked_message_ids.extend([message.id for message in messages])
        logging.info('Прослушиваю новые сообщения')
        sheet_config = SheetConfig(
            url_sheet=settings.google_sheets.config_url_sheet,
            name_work_sheet=settings.google_sheets.config_worksheet_name
        )
        drive_upload = GoogleDriveUpload()
        while True:
            messages = wh.get_new_messages(exclude_message_ids=checked_message_ids)
            for message in messages:
                short_phrase, id_ = wh.get_short_phrase_and_id(message.text)
                if not short_phrase or not id_:
                    continue
                configs = sheet_config.get_whatsapp_configs()
                exist_config = None
                for config in configs:
                    if config.short_phrase == short_phrase.replace('#', ''):
                        exist_config = config
                        break
                if (not exist_config
                        or exist_config.link_sales_sheet == ''
                        or exist_config.column_for_link_file == ''
                        or exist_config.column_order_number == ''):
                    continue
                file_path = f'./temp/{id_}.jpg'
                downloaded = wh.download_file_blob(file_path=file_path, quote=message.quote)
                if not downloaded:
                    continue
                upload_file = drive_upload.upload_file(
                    folder_id=settings.google_drive.folder_id_uploads,
                    file_path=file_path,
                    file_name=id_,
                )
                os.remove(file_path)
                if not upload_file:
                    continue
                link_file = upload_file['alternateLink']
                sheet_sales = SheetSales(
                    url_sheet=exist_config.link_sales_sheet,
                    name_work_sheet=exist_config.name_worksheet
                )
                sheet_sales.set_google_drive_url_file(
                    find_id=id_,
                    google_drive_url=link_file,
                    config=exist_config
                )
            checked_message_ids.extend([message.id for message in messages])
            time.sleep(settings.selenium.timeout_get_messages)
    except (Exception,):
        logging.error('Ошибка')
        traceback.print_exc()
    finally:
        driver.quit()
        driver.close()
        input()


if __name__ == '__main__':
    main()
