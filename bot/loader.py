import logging

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from bot.config import settings, options


def get_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


logging.basicConfig(
    level=logging.INFO,
    format="%(filename)s:%(lineno)d #%(levelname)-8s "
           "[%(asctime)s] - %(name)s - %(message)s",
)

checked_message_ids = []
