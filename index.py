#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
from libs.cli_router import main

#
# INSTRUCCIONES
#

login_data = {
    'site_url': 'https://torrepadregourmet.es',
    'log': 'pablo@tiendaonline.com.ar',
    'pwd': 'pablo123$=Nn',
    'login_page': 'wp-login.php',
    'cart_page': '/cart/'
}

cart_page = '/cart/'

order_to_exe = [
    {
        'prd': '/producto/queso-oregano-530gr/',
        'qty': 2
    },
    {
        'prd': '/producto/jamon-de-tudanca/',
        'qty': 5
    },
    {
        'prd': '/producto/chorizo-de-ciervo-300g/',
        'qty': 3
    }
]

def setup():
    options = Options()
    options.add_extension("D:\ChromeExtensions\DarkReader.crx")
    # options.add_argument("--headless")
    # options.add_argument('--headless=new')
    # options.add_argument("start-maximized")
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--disable-gpu')
    # options.add_argument('--no-sandbox')
    # option.binary_location = "/path/to/google-chrome"

    driver = webdriver.Chrome(options=options)

    # driver = webdriver.Chrome(service=ChromeService(
    #     ChromeDriverManager().install()), options=options)

    # Cierra la pestaña del DarkReader
    main_window = driver.current_window_handle
    dark_reader_window = None

    for window_handle in driver.window_handles:
        if window_handle != main_window:
            dark_reader_window = window_handle
            break

    if dark_reader_window:
        driver.switch_to.window(dark_reader_window)
        driver.close()

    # Vuelve a la ventana principal
    driver.switch_to.window(main_window)
    
    return driver


def login(login_data):
    driver.get(login_data['site_url'] + '/' + login_data['login_page'])

    username_input = driver.find_element(By.ID, 'user_login')
    username_input.send_keys(login_data['log'])

    password_input = driver.find_element(By.ID, 'user_pass')
    password_input.send_keys(login_data['pwd'])

    login_button = driver.find_element(By.ID, 'wp-submit')
    login_button.click()

def get_cart_items():
    driver.get(login_data['site_url'] + cart_page)
    time.sleep(5)

    cart_items = []

    product_rows = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.woocommerce-cart-form__cart-item"))
    )

    for row in product_rows:
        product_name_element = row.find_element(By.CSS_SELECTOR, "td.product-name a")
        product_name = product_name_element.text
        product_url = product_name_element.get_attribute("href")

        product_price_element = row.find_element(By.CSS_SELECTOR, "td.product-price span.woocommerce-Price-amount")
        product_price = product_price_element.text

        product_quantity_element = row.find_element(By.CSS_SELECTOR, "td.product-quantity input.input-text.qty.text")
        product_quantity = product_quantity_element.get_attribute("value")

        product_subtotal_element = row.find_element(By.CSS_SELECTOR, "td.product-subtotal span.woocommerce-Price-amount")
        product_subtotal = product_subtotal_element.text

        cart_items.append({
            'name': product_name,
            'url': product_url,
            'price': product_price,
            'quantity': product_quantity,
            'subtotal': product_subtotal
        })

    return cart_items

def print_cart_items(cart_items):
    print("[ CART ] -----------------------------\r\n")
    for item in cart_items:
        print("Name:", item['name'])
        print("URL:", item['url'])
        print("Price:", item['price'])
        print("Quantity:", item['quantity'])
        print("Subtotal:", item['subtotal'])
        print()
    print("--------------------------------------\r\n")

class Product: 
    @staticmethod
    def print(self):
        print("Title:", self.title)
        print("Price:", self.price)
        print("Stock:", self.stock)
        print("SKU:", self.sku)
        print("--------------------------------------\r\n")

def get_product(product_url=None):
    if product_url is not None:
        driver.get(login_data['site_url'] + product_url)
        time.sleep(2)

    p = Product()

    title_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h1[@class='product-title product_title entry-title']"))
    )
    p.title = title_element.text


    price_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='product-main']//bdi[1]"))
    )
    p.price = price_element.text

    description_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='product-short-description']/p"))
    )
    p.description = description_element.text

    stock_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "p.stock.in-stock"))
    )
    p.stock = stock_element.text

    sku_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "span.sku"))
    )
    p.sku = sku_element.text

    # Retorna un objeto Producto
    return p


if __name__ == "__main__":
    main(sys.argv[1:])


#
# Initial Setup
#

driver = setup()

try:
    #
    # Login
    #
    
    login(login_data)

    driver.maximize_window()

    #
    # Carrito
    #

    cart_items = get_cart_items()
    print_cart_items(cart_items)


    #
    # Orden
    #

    print("COMIENZO A EJECUTAR LA ORDEN: --->\r\n")
    for order in order_to_exe:
        product_page = order['prd']
        quantity = order['qty']

        driver.get(login_data['site_url'] + product_page)
        time.sleep(2)

        p = get_product()
        Product.print(p)

        quantity_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.quantity.buttons_added input[type='number'][name='quantity']"))
        )

        quantity_input.clear()
        quantity_input.send_keys(str(quantity))

        add_to_cart_button = driver.find_element(By.CSS_SELECTOR, "button.single_add_to_cart_button")
        add_to_cart_button.click()
        time.sleep(3)
    print("FINALIZADA LA EJECUCION DE LA ORDEN <---\r\n")

    #
    # Carrito
    #

    cart_items = get_cart_items()
    print_cart_items(cart_items)


finally:
    time.sleep(3)
    driver.quit()
