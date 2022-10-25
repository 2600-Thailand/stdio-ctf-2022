from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import os
import time

def getEnv(env, fallback):
    if env in os.environ:
        return os.environ.get(env)
    else:
        return fallback

URL = "http://localhost:8000"
ADMIN_PASSWORD = getEnv("ADMIN_PASSWORD", "HelloWorld")

def get_driver(waitLoad=True):
    # Use most flag from https://ctftime.org/writeup/27727
    options = Options()
    options.add_argument('headless')
    options.add_argument('no-sandbox')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('disable-infobars')
    options.add_argument('disable-background-networking')
    options.add_argument('disable-default-apps')
    options.add_argument('disable-extensions')
    options.add_argument('disable-gpu')
    options.add_argument('disable-sync')
    options.add_argument('disable-translate')
    options.add_argument('hide-scrollbars')
    options.add_argument('metrics-recording-only')
    options.add_argument('mute-audio')
    options.add_argument('no-first-run')
    options.add_argument('dns-prefetch-disable')
    options.add_argument('safebrowsing-disable-auto-update')
    options.add_argument('media-cache-size=1')
    options.add_argument('disk-cache-size=1')
    options.add_argument('user-agent=CTFAdmin/1.0')
    if waitLoad == True:
        driver = webdriver.Chrome('chromedriver', options=options)
    else:
        d = DesiredCapabilities.CHROME
        d['pageLoadStrategy'] = "none"
        driver = webdriver.Chrome('chromedriver', options=options, desired_capabilities=d)
        driver.set_script_timeout(6);
        driver.set_page_load_timeout(6);
    return driver

def get_cookies():
    driver = get_driver()
    driver.get(f'{URL}/auth/login')

    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    username_field.send_keys("admin")
    password_field.send_keys(ADMIN_PASSWORD)
    driver.find_element(By.NAME, "submit").click()

    WebDriverWait(driver=driver, timeout=10).until(
        lambda x: x.execute_script("return document.readyState === 'complete'")
    )
    try:
        errors = driver.find_element(By.CLASS_NAME, "flash")
        if errors:
            raise("FAIL TO LOGIN")
    except:
       print("Login Success")
    return driver.get_cookies()

def visit_report(cookies):
    driver = get_driver(waitLoad=False)
    driver.get(f'{URL}/auth/login')
    WebDriverWait(driver, 5).until(lambda r: r.execute_script('return document.readyState') == 'complete')
    for cookie in cookies:
        driver.add_cookie({'name': cookie["name"], 'value': cookie["value"], 'httpOnly': True})
    try:
        driver.get(f'{URL}/admin/')
        WebDriverWait(driver, 5).until(lambda r: r.execute_script('return document.readyState') == 'complete')
    except:
        pass
    finally:
        driver.quit()

cookies = get_cookies()
while True:
    try:
        visit_report(cookies)
        time.sleep(1)
    except Exception as e:
        print(e) # The exception shouldn't reach here so it's critical
