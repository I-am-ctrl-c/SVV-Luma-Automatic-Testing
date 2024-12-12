import random
import logging
import numpy as np
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

bTime = 0

# Configure logging
logging.basicConfig(
    filename="test_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def xFinds(xpath: str, parent_element=None):
    try:
        if parent_element is None:
            parent_element = driver
        return parent_element.find_elements(By.XPATH, xpath)
    except Exception as e:
        logging.error(f"Error finding elements by XPath '{xpath}': {e}")
        return []

def xFind(xpath: str, parent_element=None):
    try:
        if parent_element is None:
            parent_element = driver
        return parent_element.find_element(By.XPATH, xpath)
    except Exception as e:
        logging.error(f"Error finding element by XPath '{xpath}': {e}")
        return None

def cFinds(classname: str, parent_element=None):
    try:
        if parent_element is None:
            parent_element = driver
        return parent_element.find_elements(By.CLASS_NAME, classname)
    except Exception as e:
        logging.error(f"Error finding elements by class name '{classname}': {e}")
        return []

def CSSFinds(classname: str, parent_element=None):
    try:
        if parent_element is None:
            parent_element = driver
        return parent_element.find_elements(By.CSS_SELECTOR, classname)
    except Exception as e:
        logging.error(f"Error finding elements by CSS selector '{classname}': {e}")
        return []

def CSSFind(classname: str, parent_element=None):
    try:
        if parent_element is None:
            parent_element = driver
        return parent_element.find_element(By.CSS_SELECTOR, classname)
    except Exception as e:
        logging.error(f"Error finding element by CSS selector '{classname}': {e}")
        return None

def login():
    _SignIn = xFind('/html/body/div[2]/header/div[1]/div/ul/li[2]/a')
    if _SignIn:
        _SignIn.click()
    _Email = xFind('/html/body/div[2]/main/div[3]/div/div[2]/div[1]/div[2]/form/fieldset/div[2]/div/input')
    _Password = xFind('/html/body/div[2]/main/div[3]/div/div[2]/div[1]/div[2]/form/fieldset/div[3]/div/input')
    if _Email and _Password:
        _Email.send_keys('zhang.23519@gmail.com')
        _Password.send_keys('123456zzZZ')
    _SignIn = xFind('//*[@id="send2"]/span')
    if _SignIn:
        _SignIn.click()
    logging.info("Login completed")

def add_products():
    global bTime
    cloth = ['//*[@id="ui-id-11"]', '//*[@id="ui-id-12"]', '//*[@id="ui-id-13"]', '//*[@id="ui-id-14"]', '//*[@id="ui-id-19"]', '//*[@id="ui-id-20"]', '//*[@id="ui-id-21"]', '//*[@id="ui-id-22"]']
    times = random.randint(1, 3)
    all_items = []
    logging.info(f"Adding products {times} times.")
    for j in range(times):
        category = random.choice(cloth)
        _CategoryElement = xFind(category)
        if _CategoryElement:
            driver.execute_script("arguments[0].click();", _CategoryElement)
        else:
            continue
        items = []
        numbers = random.randint(1, 3)
        logging.info(f"Adding {numbers} products.")
        for i in range(numbers):
            products = cFinds('product-image-photo')
            if not products:
                continue
            product = random.choice(products)
            driver.execute_script("arguments[0].click();", product)

            _Name = xFind('//*[@id="maincontent"]/div[2]/div/div[1]/div[1]/h1/span')
            if not _Name:
                continue

            _Sizes = CSSFinds('div.swatch-option.text')
            if _Sizes:
                _Size = random.choice(_Sizes)
                size = _Size.text
                driver.execute_script("arguments[0].click();", _Size)
            else:
                size = "Unknown"

            _Colors = CSSFinds('div.swatch-option.color')
            if _Colors:
                _Color = random.choice(_Colors)
                color = _Color.get_dom_attribute("option-label")
                driver.execute_script("arguments[0].click();", _Color)
            else:
                color = "Unknown"

            _Qty = CSSFind('.input-text.qty')
            if not _Qty:
                continue
            _Qty.clear()
            if random.randint(1, 100) <= 50:
                p = random.randint(0, 5)
                outOfBound = [-1, 0, 10000, 10001, 2147483647, 2147483648]
                num = outOfBound[p]
            else:
                num = random.randint(1, 100)

            _Qty.send_keys(str(num))

            if num < 1 or num > 100:
                bTime += 1
                _Qty.clear()
                num = random.randint(1, 100)
                _Qty.send_keys(str(num))

            _Price = CSSFind('[data-price-type="finalPrice"]')
            if not _Price:
                continue
            price = float(_Price.get_dom_attribute('data-price-amount'))

            _Photo = CSSFind('img[aria-hidden="false"]')
            if _Photo:
                src = _Photo.get_dom_attribute('src').rsplit('/', 1)[-1]
            else:
                src = "Unknown"

            span_element = xFind('//span[normalize-space(text())="Add to Cart"]')
            if span_element:
                driver.execute_script("arguments[0].click();", span_element)

            items.append((_Name.text, src, size, color, num, price))
            logging.info(f"Added product: {_Name.text}, Size: {size}, Color: {color}, Quantity: {num}, Price: {price}")

            driver.back()
        all_items.append(items)
    return all_items

def check_shopping_cart(all_items):
    _Button = xFind('//html/body/div[2]/header/div[2]/div[1]/div/div/div/div[2]/div[5]/div/a/span')
    if _Button:
        driver.execute_script("arguments[0].click();", _Button)
    else:
        return None
    Names = xFinds('//*[@id="shopping-cart-table"]/tbody/tr/td[1]/div/strong/a')
    Colors = xFinds('//*[@id="shopping-cart-table"]/tbody/tr[1]/td[1]/div/dl/dd[2]')
    Sizes = xFinds('//*[@id="shopping-cart-table"]/tbody/tr[1]/td[1]/div/dl/dd[1]')
    Qtys = xFinds('/html/body/div[2]/main/div[3]/div/div[2]/form/div[1]/table/tbody/tr[1]/td[3]/div/div/label/input')
    Srcs = xFinds('/html/body/div[2]/main/div[3]/div/div[2]/form/div[1]/table/tbody/tr[1]/td[1]/a/span/span/img')
    cart_items = []

    for name, src, color, size, qty in zip(Names, Srcs, Colors, Sizes, Qtys):
        cart_items.append({
            "name": name.text.strip(),
            "src": src.get_dom_attribute("src").rsplit('/', 1)[-1],
            "color": color.text.strip(),
            "size": size.text.strip(),
            "qty": int(qty.get_dom_attribute("value")),
        })
    logging.info(f"Shopping cart content: {cart_items}")

    consistent = True
    for recorded_items in all_items:
        for recorded_item in recorded_items:
            rec_name, src, size, color, num, price = recorded_item
            matched = any(
                rec_name == item["name"] and  # 比较商品名字
                item["color"] == color and  # 比较颜色
                item["size"] == size and
                item["src"] == src and
                item["qty"] == num  # 比较数量
                for item in cart_items
            )
            if not matched:
                consistent = False
                logging.error(f"Recorded item: {recorded_item} error")
                print("\nDiscrepancy found:")
                print(f"Recorded item: {recorded_item}")
                for item in cart_items:
                    print(item)
    if consistent:
        success.append(0)
        logging.info(f"Round {i + 1} success, total covered {bTime} boundary value")
    else:
        success.append(1)
        print("\nSome items do not match between added products and shopping cart.")
        logging.error(f"Round {i + 1} error")

def add_shopping_cart():
    all_items = add_products()
    if all_items:
        check_shopping_cart(all_items)

def plot_success_rate(results):
    # 绘制成功测试比例的饼图
    successes = results.count(0)
    failures = len(results) - successes
    labels = ['Success', 'Failure']
    sizes = [successes, failures]

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#4CAF50', '#F44336'])
    plt.title("Success Rate")
    plt.savefig("success_rate_pie_chart.png")
    plt.show()


if __name__ == '__main__':
    opt = Options()
    opt.add_experimental_option('detach', True)
    driver = webdriver.Chrome(service=Service('chromedriver.exe'), options=opt)
    driver.implicitly_wait(10)

    success = []
    results = []
    for i in range(50):
        print(i + 1)
        driver.get('https://magento.softwaretestingboard.com/')
        seed = int(datetime.now().timestamp())
        random.seed(seed)
        logging.info(f"Round {i+1}: Using seed {seed}")

        add_shopping_cart()
        results.append(bTime)
        driver.delete_all_cookies()  # Clear cookies
        driver.get('about:blank')
    plot_success_rate(success)
    print(results)
