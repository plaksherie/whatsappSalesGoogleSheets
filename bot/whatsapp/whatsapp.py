import base64
import logging
import re
import time
import traceback
from typing import List, Union

import pyperclip
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bot.whatsapp.message import WhatsappMessage


class Whatsapp:
    BASE_URL = 'https://web.whatsapp.com'
    selector_qr_code = 'canvas[aria-label="Scan me!"]'
    selector_search_chats = 'div[contenteditable="true"][title="Текстовое поле поиска"]'
    selector_search_items = 'div[aria-label="Результаты поиска."] div[role="listitem"]'
    selector_search_item_title = 'span[aria-label][title]'
    selector_messages = 'div[role="application"] > div[role="row"]'
    selector_message_text = 'span.selectable-text.copyable-text span'
    selector_message_id = 'div[data-id]'
    selector_message_quote = 'div[role="button"][aria-label="Процитированное сообщение"]'
    xpath_message_quote_images = './/div[contains(@style, "background-image")]'
    TIMEOUTS = {
        selector_qr_code: 20,
        selector_search_chats: 10,
        selector_messages: 10,
    }
    REGULAR_FIND_BLOB_URL = r'background-image:\s*url\("blob:(.+?)"\);'

    def __init__(
            self,
            driver: webdriver.Chrome
    ) -> None:
        self.driver = driver

    def enter_site(
            self,
    ) -> bool:
        self.driver.get(self.BASE_URL)
        login = True
        try:
            qr_code = WebDriverWait(self.driver, self.TIMEOUTS[self.selector_qr_code]).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.selector_qr_code))
            )
            if qr_code:
                login = False
        except TimeoutException:
            login = True
        return login

    def search_chat(
            self,
            chat_name: str,
    ) -> None:
        try:
            search_chats = WebDriverWait(self.driver, self.TIMEOUTS[self.selector_search_chats]).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.selector_search_chats))
            )
            search_chats.click()
            # self.driver.execute_script("arguments[0].innerHTML = '{}'".format(chat_name), search_chats)
            # search_chats.send_keys('.')
            # search_chats.send_keys(Keys.BACKSPACE)
            # pyperclip.copy(chat_name)
            # action = ActionChains(self.driver)
            # action.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            self.driver.execute_script(f'''
                            const text = `{chat_name}`;
                            const dataTransfer = new DataTransfer();
                            dataTransfer.setData('text', text);
                            const event = new ClipboardEvent('paste', {{
                              clipboardData: dataTransfer,
                              bubbles: true
                            }});
                            arguments[0].dispatchEvent(event)
                            ''', search_chats)
        except (Exception,):
            logging.error('Ошибка при поиске чата')
            traceback.print_exc()

    def enter_to_chat(
            self,
            chat_name: str
    ) -> None:
        self.search_chat(chat_name)
        time.sleep(2)
        search_chats = self.driver.find_elements(By.CSS_SELECTOR, self.selector_search_items)
        for chat in search_chats:
            title = chat.find_element(By.CSS_SELECTOR, self.selector_search_item_title)
            if title and title.get_attribute('title') == chat_name:
                chat.click()
                try:
                    WebDriverWait(self.driver, self.TIMEOUTS[self.selector_messages]).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, self.selector_messages))
                    )
                except TimeoutException:
                    logging.error(f'Не найдено сообщений при входе в чат {chat_name}')
                else:
                    logging.info(f'Вошел в чат {chat_name}')
                break

    def parse_message(
            self,
            raw_message: WebElement
    ) -> WhatsappMessage:
        message_id = raw_message.find_element(By.CSS_SELECTOR, self.selector_message_id).get_attribute('data-id')
        try:
            text = raw_message.find_element(By.CSS_SELECTOR, self.selector_message_text).text
        except NoSuchElementException:
            text = ''
        try:
            quote = raw_message.find_element(By.CSS_SELECTOR, self.selector_message_quote)
        except NoSuchElementException:
            quote = None
        return WhatsappMessage(id=message_id, quote=quote, text=text)

    def get_new_messages(
            self,
            exclude_message_ids: List[str] = None,
            only_quote: bool = True
    ) -> List[WhatsappMessage]:
        new_messages = self.driver.find_elements(By.CSS_SELECTOR, self.selector_messages)
        messages = []
        for message_raw in new_messages:
            new_message = self.parse_message(message_raw)
            if not new_message.quote and only_quote:
                continue
            if exclude_message_ids and new_message.id in exclude_message_ids:
                continue
            messages.append(new_message)

        return messages

    def get_url_image_in_quote(
            self,
            quote: WebElement
    ) -> str | None:
        url = None
        bg_images = quote.find_elements(By.XPATH, self.xpath_message_quote_images)
        for bg in bg_images:
            style_attribute = bg.get_attribute("style")
            pattern = re.compile(self.REGULAR_FIND_BLOB_URL)
            match = pattern.search(style_attribute)
            if match:
                url = match.group(1)
                break
        return url

    def download_file_blob(
            self,
            file_path: str,
            quote: WebElement
    ) -> bool:
        try:
            url = self.get_url_image_in_quote(quote)
            blob_data = self.driver.execute_script("return (async () => { \
                const response = await fetch(arguments[0]); \
                const blob = await response.blob(); \
                return new Promise((resolve, reject) => { \
                    const reader = new FileReader(); \
                    reader.onloadend = () => resolve(reader.result); \
                    reader.onerror = reject; \
                    reader.readAsDataURL(blob); \
                }); \
            })(arguments[0]);", f'blob:{url}')
            ext, binary_data = blob_data.split(",")
            binary_data = binary_data.encode("utf-8")
            with open(file_path, "wb") as file:
                file.write(base64.b64decode(binary_data, validate=True))
            return True
        except (Exception,):
            logging.error('Ошибка в скачивании файла')
            traceback.print_exc()
            return False

    @staticmethod
    def get_short_phrase_and_id(text: str) -> tuple[str | None, str | None]:
        short_phrase = None
        id_ = text.split('\n')[1] if len(text.split('\n')) > 0 else None
        search_short_phrase = re.search(r'#(\w+)', text)
        # search_id_ = re.search(r'\n(\d+)', text)
        if search_short_phrase:
            short_phrase = search_short_phrase.group(1)
        # if search_id_:
        #     id_ = search_id_.group(1)
        return short_phrase, id_
