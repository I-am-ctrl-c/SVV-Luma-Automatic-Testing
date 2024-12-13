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

# 将相关选择器提取到字典中统一管理
SELECTORS = {
    "sign_in_link": '/html/body/div[2]/header/div[1]/div/ul/li[2]/a',
    "email_input": '/html/body/div[2]/main/div[3]/div/div[2]/div[1]/div[2]/form/fieldset/div[2]/div/input',
    "password_input": '/html/body/div[2]/main/div[3]/div/div[2]/div[1]/div[2]/form/fieldset/div[3]/div/input',
    "login_button": '//*[@id="send2"]/span',

    # 分类页面
    "categories": [
        '//*[@id="ui-id-11"]', '//*[@id="ui-id-12"]', '//*[@id="ui-id-13"]', '//*[@id="ui-id-14"]',
        '//*[@id="ui-id-19"]', '//*[@id="ui-id-20"]', '//*[@id="ui-id-21"]', '//*[@id="ui-id-22"]'
    ],

    # 产品详情页
    "product_name": '//*[@id="maincontent"]/div[2]/div/div[1]/div[1]/h1/span',
    "size_options": 'div.swatch-option.text',
    "color_options": 'div.swatch-option.color',
    "qty_input": '.input-text.qty',
    "price_element": '[data-price-type="finalPrice"]',
    "photo_element": 'img[aria-hidden="false"]',
    "add_to_cart_button": '//span[normalize-space(text())="Add to Cart"]',

    # 购物车
    "cart_button": '/html/body/div[2]/header/div[2]/div[1]/div/div/div/div[2]/div[5]/div/a/span',
    "cart_item_names": '//*[@id="shopping-cart-table"]/tbody/tr/td[1]/div/strong/a',
    "cart_item_colors": '//*[@id="shopping-cart-table"]/tbody/tr[1]/td[1]/div/dl/dd[2]',
    "cart_item_sizes": '//*[@id="shopping-cart-table"]/tbody/tr[1]/td[1]/div/dl/dd[1]',
    "cart_item_qtys": '/html/body/div[2]/main/div[3]/div/div[2]/form/div[1]/table/tbody/tr[1]/td[3]/div/div/label/input',
    "cart_item_srcs": '/html/body/div[2]/main/div[3]/div/div[2]/form/div[1]/table/tbody/tr[1]/td[1]/a/span/span/img',

    # 产品列表页面
    "product_images": 'product-image-photo'
}

# Configure logging
logging.basicConfig(
    filename="test_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def xFinds(xpath: str, parent_element=None):
    """Find multiple elements by XPath"""
    try:
        if parent_element is None:
            parent_element = driver
        return parent_element.find_elements(By.XPATH, xpath)
    except Exception as e:
        logging.error(f"Error finding elements by XPath '{xpath}': {e}")
        return []

def xFind(xpath: str, parent_element=None):
    """Find a single element by XPath"""
    try:
        if parent_element is None:
            parent_element = driver
        return parent_element.find_element(By.XPATH, xpath)
    except Exception as e:
        logging.error(f"Error finding element by XPath '{xpath}': {e}")
        return None

def cFinds(classname: str, parent_element=None):
    """Find multiple elements by class name"""
    try:
        if parent_element is None:
            parent_element = driver
        return parent_element.find_elements(By.CLASS_NAME, classname)
    except Exception as e:
        logging.error(f"Error finding elements by class name '{classname}': {e}")
        return []

def CSSFinds(selector: str, parent_element=None):
    """Find multiple elements by CSS selector"""
    try:
        if parent_element is None:
            parent_element = driver
        return parent_element.find_elements(By.CSS_SELECTOR, selector)
    except Exception as e:
        logging.error(f"Error finding elements by CSS selector '{selector}': {e}")
        return []

def CSSFind(selector: str, parent_element=None):
    """Find a single element by CSS selector"""
    try:
        if parent_element is None:
            parent_element = driver
        return parent_element.find_element(By.CSS_SELECTOR, selector)
    except Exception as e:
        logging.error(f"Error finding element by CSS selector '{selector}': {e}")
        return None

def login():
    """Perform login operation"""
    _SignIn = xFind(SELECTORS["sign_in_link"])
    if _SignIn:
        _SignIn.click()
    _Email = xFind(SELECTORS["email_input"])
    _Password = xFind(SELECTORS["password_input"])
    if _Email and _Password:
        _Email.send_keys('zhang.23519@gmail.com')
        _Password.send_keys('123456zzZZ')
    _SignIn = xFind(SELECTORS["login_button"])
    if _SignIn:
        _SignIn.click()
    logging.info("Login completed")

def add_products():
    """
    Randomly select categories and products, add them to cart.
    Returns:
        all_items: List of lists containing added product info.
    """
    global bTime
    cloth = SELECTORS["categories"]
    times = random.randint(1, 3)
    all_items = []
    logging.info(f"Adding products {times} times.")
    for _ in range(times):
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
            products = cFinds(SELECTORS["product_images"])
            if not products:
                continue
            product = random.choice(products)
            driver.execute_script("arguments[0].click();", product)

            _Name = xFind(SELECTORS["product_name"])
            if not _Name:
                driver.back()
                continue

            _Sizes = CSSFinds(SELECTORS["size_options"])
            if _Sizes:
                _Size = random.choice(_Sizes)
                size = _Size.text
                driver.execute_script("arguments[0].click();", _Size)
            else:
                size = "Unknown"

            _Colors = CSSFinds(SELECTORS["color_options"])
            if _Colors:
                _Color = random.choice(_Colors)
                color = _Color.get_dom_attribute("option-label")
                driver.execute_script("arguments[0].click();", _Color)
            else:
                color = "Unknown"

            _Qty = CSSFind(SELECTORS["qty_input"])
            if not _Qty:
                driver.back()
                continue
            _Qty.clear()

            # 边界值测试
            if random.randint(1, 100) <= 50:
                outOfBound = [-1, 0, 10000, 10001, 2147483647, 2147483648]
                num = random.choice(outOfBound)
            else:
                num = random.randint(1, 100)

            _Qty.send_keys(str(num))
            if num < 1 or num > 100:
                bTime += 1
                _Qty.clear()
                num = random.randint(1, 100)
                _Qty.send_keys(str(num))

            _Price = CSSFind(SELECTORS["price_element"])
            if not _Price:
                driver.back()
                continue
            price = float(_Price.get_dom_attribute('data-price-amount'))

            _Photo = CSSFind(SELECTORS["photo_element"])
            if _Photo:
                src = (_Photo.get_dom_attribute('src').rsplit('/', 1)[-1])
                src = src.replace("_main_", "").replace("_back_", "")
            else:
                src = "Unknown"

            span_element = xFind(SELECTORS["add_to_cart_button"])
            if span_element:
                driver.execute_script("arguments[0].click();", span_element)

            items.append((_Name.text, src, size, color, num, price))
            logging.info(f"Added product: {_Name.text}, Size: {size}, Color: {color}, Quantity: {num}, Price: {price}")

            driver.back()
        all_items.append(items)
    return all_items

def check_shopping_cart(all_items):
    """
    Check that the products in the shopping cart match the recorded items.
    """
    _Button = xFind(SELECTORS["cart_button"])
    if _Button:
        driver.execute_script("arguments[0].click();", _Button)
    else:
        return None

    Names = xFinds(SELECTORS["cart_item_names"])
    Colors = xFinds(SELECTORS["cart_item_colors"])
    Sizes = xFinds(SELECTORS["cart_item_sizes"])
    Qtys = xFinds(SELECTORS["cart_item_qtys"])
    Srcs = xFinds(SELECTORS["cart_item_srcs"])

    cart_items = []
    for name, src, color, size, qty in zip(Names, Srcs, Colors, Sizes, Qtys):
        temp = src.get_dom_attribute("src").rsplit('/', 1)[-1].replace("_back_", "")
        temp = temp.replace("_main_", "")
        cart_items.append({
            "name": name.text.strip(),
            "src": temp,
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
                rec_name == item["name"] and
                item["color"] == color and
                item["size"] == size
                and item["src"] == src
                and item["qty"] == num
                for item in cart_items
            )
            if not matched:
                consistent = False
                logging.error(f"Recorded item: {recorded_item} not found in cart properly.")
                print("\nDiscrepancy found:")
                print(f"Recorded item: {recorded_item}")
                print("Cart items were:")
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
    """
    Add products and check the shopping cart.
    """
    all_items = add_products()
    if all_items:
        check_shopping_cart(all_items)

def edit_shopping_cart():
    random.seed(3)
    all_items = add_products()
    _Button = xFind(SELECTORS["cart_button"])
    if _Button:
        driver.execute_script("arguments[0].click();", _Button)
    dele = xFinds('//*[@id="shopping-cart-table"]/tbody/tr[2]/td/div/a[2]')
    if dele:
        for i in range(random.randint(1, len(dele) - 1)):
            _Button = random.choice(dele)
            driver.execute_script("arguments[0].click();", _Button)


def plot_success_rate(results):
    """
    Plot a pie chart for success/failure rate.
    """
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
    # opt = Options()
    # opt.add_experimental_option('detach', True)
    # driver = webdriver.Chrome(service=Service('chromedriver.exe'), options=opt)
    # driver.implicitly_wait(10)
    #
    # success = []
    # results = []
    # rounds = 50
    # for i in range(rounds):
    #     print(i + 1)
    #     driver.get('https://magento.softwaretestingboard.com/')
    #     seed = int(datetime.now().timestamp())
    #     random.seed(seed)
    #     logging.info(f"Round {i+1}: Using seed {seed}")
    #
    #     add_shopping_cart()
    #     results.append(bTime)
    #     driver.delete_all_cookies()  # Clear cookies
    #     driver.get('about:blank')
    #
    # plot_success_rate(success)
    # print(f"Cover boundary:{bTime} times")
    # print("Success array:", success)
    # logging.info(f"Final success list: {success}")
    # driver.quit()



    opt = Options()
    opt.add_experimental_option('detach', True)
    driver = webdriver.Chrome(service=Service('chromedriver.exe'), options=opt)
    driver.implicitly_wait(10)

    success = []
    results = []
    rounds = 50
    for i in range(rounds):
        print(i + 1)
        driver.get('https://magento.softwaretestingboard.com/')
        seed = 1
        random.seed(seed)
        logging.info(f"Round {i+1}: Using seed {seed}")

        edit_shopping_cart()
        results.append(bTime)
        driver.delete_all_cookies()  # Clear cookies
        driver.get('about:blank')

    plot_success_rate(success)
    print(f"Cover boundary:{bTime} times")
    print("Success array:", success)
    logging.info(f"Final success list: {success}")
    driver.quit()

