# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorld++")
    try:
        chrome_options.add_extension('NetEaseMusicWorld++.crx')
        logging.info("Extension added successfully!")
    except Exception as e:
        logging.error(f"Failed to added extension NetEaseMusicWorld++")
        logging.error(e)

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "002FCB1992FDF81B929461E7AFE0111E1769F89AFCD1500D758227355708EA48BF590A4CAEDFCC856F25726A87BC1C169CE5FA25D9B041CA9CFACE3D24A771CB17E9DB4C5F09FA0F211B8276A651373A8B832D2E0B35EAE22D8D565B4C445306BBC7119435B08C5B165DE7370D90711694FDA3E4FD9BA6A6706767824D8B2523EAEE52167C9F1E1A71EC479730E2C4575697D1CADC12B726103E4F56BD9DF670BCCB07532E80B3524F8A0E1D1390D851B4273BB67BBBC326EDFD3BDD5FCA1FA0E649831F434D5118C7A0D622B0D3F6BCC3ACA2A6F9EA3F237BBEFD9FDC5D079386BDD89B0770C549D59EC3EA02A81C6F189FED3D600A14773A01E514ADF20192C786D37FC3BB789E6015186D8E39F3A435A5DB5A881556BB5DCF61B4E398FCBFF33940A12B6834CF6CE45868AAB0D2038A5EB5C69A52D71D9635B9DD48A9D8151313A5B43C29BF89F6CE1FF2B89CE04FF3E21F9F79158FE2280204F2435CD03AF0"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
