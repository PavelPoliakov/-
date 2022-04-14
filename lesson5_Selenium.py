from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import exceptions
from pymongo import MongoClient
import time

client = MongoClient('127.0.0.1', 27017)
db = client['goods']
mvideo = db.mvideo

options = Options()
options.add_argument("start-maximized")

s = Service('./chromedriver')
driver = webdriver.Chrome(service=s, options=options)

driver.get('https://www.mvideo.ru/')

driver.execute_script("window.scrollTo(0, 1080);")
time.sleep(5)

#Кликнуть по кнопке "В тренде" так и не удалось
wait = WebDriverWait(driver, 10)

# try:
#     wait.until(EC.element_to_be_clickable((By.XPATH, "//mvid-shelf-group/*//span[contains(text(), 'В тренде')]/ancestor::button"))).click()
# или     driver.find_element(By.XPATH, "//mvid-shelf-group/*//span[contains(text(), 'В тренде')]/ancestor::button").click()
# except exceptions.NoSuchElementException:
#     print("***")

goods = driver.find_elements(By.XPATH, "//mvid-shelf-group//mvid-product-cards-group//div[@class='title']")

goods_list = []
for good in goods:
    good_dict = {}
    link = good.find_element(By.TAG_NAME, "a").get_attribute("href")
    name = good.find_element(By.TAG_NAME, "a").text
    good_dict['link'] = link
    good_dict['name'] = name

    goods_list.append(good_dict)

for good in goods_list:
    if mvideo.find_one({'link': good['link']}):
        print(f"Товар по ссылке {good['link']} уже существует в базе данных")
    else:
        mvideo.insert_one(good)

