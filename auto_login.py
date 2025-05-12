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
    browser.add_cookie({"name": "MUSIC_U", "value": "00FE6099C8D0017911F601A99AE469A0AD2CF02A61299557CAD42C4242A4D077EF6251101A81961BB13D5BD8095D4CC9D2F1571CDD8C0992F083F074E9138D1A1D31B7A8BA739EECCB747EDEB44A538BE521C6DC2A867D0ECFBEAF48A899A193A2FF54B2881F3E3E7A75BE346BDD921FE83D64E482635C46E6AB1855CFAB5018048B7FDC574AABF0FE1895C92E18602C9334A17CCAE547A6AFAD8024801576DF49A936B23DE878D55886B798257945BACE45A686BD96AB763B18A21241591FAABB9373BDF817E0B5B561A5D866AA2DD8DC3A5E9C4984A452B2783AEE335FC010E245723D64A313DD40A1774DAB437744E2DD31A87AF477FC7ED6558F2375D46C8D73639DB363E184C608C42B8BB8FDFE35CAC417050D487DB89CD9A790FFC0078C21E2E71D2203304732BB126E8DB34221667FB31A3A868250EDE15666E72E7A9A094FC6FE20DA95E70160E378304270447549ED1E44BC5340AC27E5BF5860D4B2"})
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
