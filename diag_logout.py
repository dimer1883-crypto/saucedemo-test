from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def run_once(i):
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1920,1080")
    d = webdriver.Chrome(options=opts)
    try:
        d.get("https://www.saucedemo.com")
        d.find_element(By.ID, "user-name").send_keys("standard_user")
        d.find_element(By.ID, "password").send_keys("secret_sauce")
        d.find_element(By.ID, "login-button").click()
        time.sleep(2)
        # logout через меню (как в реальном logout())
        d.find_element(By.ID, "react-burger-menu-btn").click()
        link = WebDriverWait(d, 10).until(EC.element_to_be_clickable((By.ID, "logout_sidebar_link")))
        print(f"[{i}] logout-link clickable, url до клика={d.current_url}")
        link.click()
        print(f"[{i}] сразу после click: url={d.current_url}")
        try:
            WebDriverWait(d, 10).until(EC.visibility_of_element_located((By.ID, "login-button")))
            print(f"[{i}] login-button появился, url={d.current_url}")
        except Exception as e:
            print(f"[{i}] ТАЙМАУТ: login-button не появился за 10с, url={d.current_url}")
    finally:
        d.quit()

for i in range(3):
    run_once(i + 1)
