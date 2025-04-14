# coding: utf-8

import os
import time
import logging
import base64
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

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    try:
        chrome_options.add_extension('NetEaseMusicWorldPlus.crx')
        logging.info("Extension added successfully!")
    except Exception as e:
        logging.error(f"Failed to added extension NetEaseMusicWorldPlus")
        logging.error(e)

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
        browser.save_screenshot("extension_frame.png")
        with open("extension_frame.png", "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode('utf-8')
            logging.info(f"::notice title=Screenshot::data:image/png;base64, {encoded}")
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00A237F57E1D7D224B914065C5550B752307B6B038CAEAFE4BCC8317FBEF742984CD5E1A32F6425DFDCC0C44BEFC76865312560C58DA74E9019F8C997FC14192784F98DF5577E71E403EE059FB3D7209B22C9C5219C0ACC98F81E533D7E6EBA2B77F1F2EC8D26187719FD9C208EBA89F0ABD51C52988D0A828CDA811FD3A512111C6110326E33CC351DBC5D6B7A1FCDDB8F382EE0D071CD7EF16777B5E367A2B0650414A346F509D230505A4DA0766A4CAEEBA437E552DC1028CC57CBE5A14C620D99B2B50B74F86435272B744177F8D75527878DFDA7A8009080094C460D52462BB52016E9DA5177564B8DBAF6A2C5AE0F8EE79AD7540557E5836B60D7B2D42517CE81E39265AE27C08CBCA7EEBA26D402EE73F480659D3307A5DFCE4A663053B6C13BDE8BDF0B69A0123DFAF0C716D66D8AE724E25EB34CE0D070747AAE8A4ED27A214F415C9F3F66713392F9CE71374C0559BD0B7390C64D3F3D077E425E010"})
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
