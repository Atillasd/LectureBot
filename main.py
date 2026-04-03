import os
import time
import logging
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('otoyoklama.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

load_dotenv()
DEU_USERNAME = os.getenv('DEU_USERNAME')
DEU_PASSWORD = os.getenv('DEU_PASSWORD')
BRAVE_PATH = os.getenv('BRAVE_PATH')

if not (DEU_USERNAME and DEU_PASSWORD and BRAVE_PATH):
    logging.critical('DEU_USERNAME, DEU_PASSWORD ve BRAVE_PATH .env içinde tanımlı olmalı')
    raise SystemExit('Gerekli ortam değişkenleri eksik.')

LOGIN_URL = 'https://online.deu.edu.tr/portal/login'
JOIN_URL = 'https://online.deu.edu.tr/portal/site/dd45d891-6374-46aa-828b-0516b9e89da9/tool/5ccb8be7-347f-43e5-b56f-838ee7253a5e'


def create_driver():
    options = Options()
    options.binary_location = BRAVE_PATH
    options.add_argument('--disable-notifications')
    options.add_argument('--start-maximized')
    return webdriver.Chrome(options=options)


def login(driver):
    driver.get(LOGIN_URL)
    logging.info('Login sayfası açıldı')

    eid_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, 'eid'))
    )
    eid_input.clear()
    eid_input.send_keys(DEU_USERNAME)

    pw_input = driver.find_element(By.ID, 'pw')
    pw_input.clear()
    pw_input.send_keys(DEU_PASSWORD)

    driver.find_element(By.ID, 'submit').click()
    logging.info('Giriş yapılıyor...')

    WebDriverWait(driver, 15).until(
        EC.url_contains('/portal')
    )

    logging.info('Giriş başarılı')


def join_meeting(driver):
    driver.get(JOIN_URL)
    logging.info('Canlı Ders sayfasına gidildi')

    rows = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'table tbody tr'))
    )
    logging.info(f'{len(rows)} toplantı satırı bulundu')

    aktif_row = None
    for i, row in enumerate(rows):
        text = row.text.strip()
        logging.info(f'Satır {i}: {text[:120]}')
        if text and 'Sonlandı' not in text:
            aktif_row = row
            logging.info(f'Aktif toplantı bulundu: Satır {i}')
            break

    if not aktif_row:
        logging.warning('Aktif toplantı bulunamadı.')
        return False

    aktif_row.click()
    time.sleep(2)

    try:
        katil_btn = WebDriverWait(driver, 12).until(
            EC.element_to_be_clickable((By.XPATH,
                "//a[contains(text(),'Toplantıya Katıl')] | //a[contains(text(),'Katıl')] | //input[contains(@value,'Katıl')] | //a[contains(text(),'Join')]"
            ))
        )
        katil_btn.click()
        logging.info('Toplantıya başarılı şekilde katılındı!')
        return True
    except Exception as e:
        logging.error('Toplantıya katılma butonu bulunamadı: %s', e)
        return False


def run_cycle():
    driver = None
    try:
        driver = create_driver()
        login(driver)
        joined = join_meeting(driver)
        if not joined:
            logging.info('Şu anda katılınacak toplantı yok veya buton bulunamadı')
    except Exception as e:
        logging.exception('Hata oluştu: %s', e)
    finally:
        if driver:
            driver.quit()
            logging.info('Tarayıcı kapatıldı')


if __name__ == '__main__':
    interval_seconds = 5 * 60  # 5 dakika

    logging.info('Otomatik yoklama döngüsü başlatıldı')
    while True:
        run_cycle()
        logging.info(f'{interval_seconds} saniye sonra tekrar denenecek')
        time.sleep(interval_seconds)



