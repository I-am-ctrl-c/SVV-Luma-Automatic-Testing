import time
import random
from os import cpu_count
from time import sleep
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def xFind(xpath: str, parent_element = None):
    if parent_element is None:
        parent_element = driver
    return parent_element.find_element(By.XPATH, xpath)

def cFinds(classname: str, parent_element = None):
    if parent_element is None:
        parent_element = driver
    return parent_element.find_elements(By.CLASS_NAME, classname)

def CSSFinds(classname: str, parent_element = None):
    if parent_element is None:
        parent_element = driver
    return parent_element.find_elements(By.CSS_SELECTOR, classname)


opt = Options()
opt.add_experimental_option('detach', True)
driver = webdriver.Chrome(service=Service('chromedriver.exe'), options=opt)
driver.implicitly_wait(10)
driver.get('https://magento.softwaretestingboard.com/')

def login():
    # log in
    _SignIn = xFind('/html/body/div[2]/header/div[1]/div/ul/li[2]/a')
    _SignIn.click()
    _Email = xFind('/html/body/div[2]/main/div[3]/div/div[2]/div[1]/div[2]/form/fieldset/div[2]/div/input')
    _Password = xFind('/html/body/div[2]/main/div[3]/div/div[2]/div[1]/div[2]/form/fieldset/div[3]/div/input')
    _Email.send_keys('zhang.23519@gmail.com')
    _Password.send_keys('123456zzZZ')
    _SignIn = xFind('//*[@id="send2"]/span')
    _SignIn.click()
    print('login is done')

# select area of products
# size and color
def add_products():
    cloth = ['//*[@id="ui-id-11"]', '//*[@id="ui-id-12"]', '//*[@id="ui-id-13"]', '//*[@id="ui-id-14"]', '//*[@id="ui-id-19"]', '//*[@id="ui-id-20"]', '//*[@id="ui-id-21"]', '//*[@id="ui-id-22"]']
    times = random.randint(1,5)
    all_items = []
    print(times)
    for j in range(times):
        driver.execute_script("arguments[0].click();", xFind( random.choice(cloth) ))

        # select clothes
        # class: product-item-photo

        items = []
        numbers = random.randint(1, 6)
        print(numbers)
        for i in range(numbers):
            products = driver.find_elements(By.CLASS_NAME, 'product-image-photo')
            product = random.choice(products)

            driver.execute_script("arguments[0].click();", product)

            _Sizes = driver.find_elements(By.CSS_SELECTOR, 'div.swatch-option.text')
            _Size = random.choice(_Sizes)
            size = _Size.text
            driver.execute_script("arguments[0].click();", _Size)

            _Colors = driver.find_elements(By.CSS_SELECTOR, 'div.swatch-option.color')
            _Color = random.choice(_Colors)
            color = _Color.get_dom_attribute("option-label")
            driver.execute_script("arguments[0].click();", _Color)

            _Qty = driver.find_element(By.CSS_SELECTOR, '.input-text.qty')
            _Qty.clear()
            num = random.randint(1, 100) # 先暂时都给正确的数字，后面再处理错误
            _Qty.send_keys(str(num))

            _Price = driver.find_element(By.CSS_SELECTOR, '[data-price-type="finalPrice"]')
            price = float(_Price.get_dom_attribute('data-price-amount'))

            _Photo = driver.find_element(By.CSS_SELECTOR, 'img[aria-hidden="false"]')
            print(_Photo)
            sleep(0.5)
            src = _Photo.get_dom_attribute('src')

            items.append((src, size, color, num, price))
            print(items[-1])

            span_element = driver.find_element(By.XPATH, '//span[normalize-space(text())="Add to Cart"]')
            driver.execute_script("arguments[0].click();", span_element)

            driver.back()
        all_items.append(items)
    print (all_items)


def check_shopping_cart():
    _Button = xFind('//html/body/div[2]/header/div[2]/div[1]/div/div/div/div[2]/div[5]/div/a/span')
    driver.execute_script("arguments[0].click();", _Button)
    # _Button.click()
    elements = driver.find_elements(By.XPATH, "//table/tbody/tr/td/div/strong/a")
    for element in elements:
        print(element.text)

login()

cloth = ['//*[@id="ui-id-11"]', '//*[@id="ui-id-12"]', '//*[@id="ui-id-13"]', '//*[@id="ui-id-14"]',
         '//*[@id="ui-id-19"]', '//*[@id="ui-id-20"]', '//*[@id="ui-id-21"]', '//*[@id="ui-id-22"]']

driver.execute_script("arguments[0].click();", xFind(random.choice(cloth)))

check_shopping_cart()