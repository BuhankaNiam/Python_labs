from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

URL = "https://eservicii.gov.md/asp/dimtcca/cerere/APO01/Edit/20ce3f0b-63fe-48e1-d4ce-08de5d1007ee"
import requests

TELEGRAM_TOKEN = "8686801883:AAGWOCY96VfKJ1oCdaitAKREu4FKE7vDy4k"
CHAT_ID = "@danilchiklolchik228"

def send_message(text):
    url = f"t.me/lovlya_mreo_bot{8686801883:AAGWOCY96VfKJ1oCdaitAKREu4FKE7vDy4k}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

driver.get(URL)

time.sleep(5)  # ждем загрузку страницы

def check_calendar():
    # открыть календарь (клик по полю)
    date_input = driver.find_element(By.CSS_SELECTOR, "input")  # возможно нужно уточнить селектор
    date_input.click()

    time.sleep(2)

    # ищем активные даты (примерный селектор!)
    days = driver.find_elements(By.CSS_SELECTOR, ".available, .active, button:not([disabled])")

    return len(days) > 0


while True:
    try:
        if check_calendar():
            print("🔥 Есть свободные даты!")
            # тут можно Telegram уведомление

        time.sleep(30)

    except Exception as e:
        print("Ошибка:", e)
        time.sleep(60)