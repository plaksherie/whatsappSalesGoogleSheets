import argparse
import os

from selenium.webdriver.chrome.options import Options

from bot.schemas.settings import Settings

parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=["dev", "prod"], default='dev')
parser.add_argument("other_args", nargs=argparse.REMAINDER)
args = parser.parse_args()
mode = args.mode

settings = Settings.get(mode)
IS_DEV = mode == 'dev'
current_directory = os.getcwd()

options = Options()
options.add_argument(f'user-agent={settings.selenium.user_agent}')
if settings.selenium.headless:
    options.add_argument('--headless=new')
options.add_argument("--window-size=1920,1080")
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--start-maximized')
options.add_argument('--disable-browser-side-navigation')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-infobars')
options.add_argument('--allow-profiles-outside-user-dir')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument(f"--user-data-dir={os.path.join(current_directory, settings.selenium.path_profiles)}")
options.add_argument(f'--profile-directory={settings.selenium.profile_name}')

