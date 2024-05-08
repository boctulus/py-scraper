import time
import sys
import os
import re
import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.firefox.options import Options as FireFoxOptions
from selenium.webdriver.firefox.service import Service as FireFoxService
from webdriver_manager.firefox import DriverManager as FireFoxDriverManager
from dotenv import load_dotenv

from libs.web_automation import WebAutomation


class MyScraper(WebAutomation):
    def __init__(self):
        self.driver = None
        self.debug  = True ###

    def setup(self, is_prod=False, install=False, web_driver='Google'):
        options = ChromeOptions() if web_driver == 'Google' else FireFoxOptions() if web_driver == 'FireFox' else None

        if options is None:
            raise ValueError(f"Unsupported web driver: {web_driver}. Supported options are 'Chrome' and 'Firefox'")
        
        if is_prod:
            # prod
            options.add_argument('--headless=new')
        else:
            # dev
            options.add_extension("DarkReader.crx")    

        # options.add_argument("--headless")
        # options.add_argument('--headless=new')
        # options.add_argument("start-maximized")
        # options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--disable-gpu')
        # options.add_argument('--no-sandbox')
        # option.binary_location = "/path/to/google-chrome"

        if install:  
            if (web_driver == 'Google'):
                self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) 

            if (web_driver == 'FireFox'):
                self.driver = webdriver.Firefox(service=ChromeService(FireFoxDriverManager().install()), options=options) 
        else:
            if (web_driver == 'Google'):
                self.driver = webdriver.Chrome(options=options)

            if (web_driver == 'FireFox'):
                self.driver = webdriver.Firefox(options=options)


    def get_cart_items(self):
        self.nav(self.cart_page)

        cart_items = []

        product_rows = self.get_all("tr.woocommerce-cart-form__cart-item")

        for row in product_rows:
            product_name     = self.get_text("td.product-name a")
            product_url      = self.get_attr("td.product-name a", "href")
            product_price    = self.get_text("td.product-price span.woocommerce-Price-amount")
            product_quantity = self.get_attr("td.product-quantity input.input-text.qty.text", "value")
            product_subtotal = self.get_text("td.product-subtotal span.woocommerce-Price-amount")

            cart_items.append({
                'name': product_name,
                'url': product_url,
                'price': product_price,
                'quantity': product_quantity,
                'subtotal': product_subtotal
            })

        return cart_items


    def print_cart_items(self, cart_items):
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

    def get_product(self, product_url=None):
        if product_url is not None:
            self.nav(product_url)

        p = self.Product()

        p.title       = self.get_text("XPATH://h1[@class='product_title entry-title']")
        p.price       = self.get_text("XPATH://div[@class='product-main']//bdi[1]")
        p.description = self.get_text("XPATH://div[@class='product-short-description']/p")
        p.stock       = self.get_text("CSS_SELECTOR:p.stock.in-stock")
        p.sku         = self.get_text("CSS_SELECTOR:span.sku")

        # Retorna un objeto Producto
        return p

    def set_checkout(self):
        self.nav(self.checkout_page)

        self.fill("XPATH://input[@id='billing_first_name']", self.order_to_exe['client']['shipping_addr']['billing_first_name'])
        self.fill("XPATH://input[@id='billing_last_name']", self.order_to_exe['client']['shipping_addr']['billing_last_name'])
        self.fill("ID:billing_address_1", self.order_to_exe['client']['shipping_addr']['billing_address_1'])
        self.fill("ID:billing_address_2", self.order_to_exe['client']['shipping_addr']['billing_address_2'])
        self.fill("ID:billing_city", self.order_to_exe['client']['shipping_addr']['billing_city'])
        self.fill("ID:billing_postcode", self.order_to_exe['client']['shipping_addr']['billing_postcode'])

        # Seleccionar el estado de facturación
        billing_state_input = self.driver.find_element(By.ID, 'select2-billing_state-container')
        billing_state_input.click()
        state_option_xpath = f"//ul[@id='select2-billing_state-results']//li[contains(text(), '{self.order_to_exe['client']['shipping_addr']['billing_state']}')]"
        state_option = self.driver.find_element(By.XPATH, state_option_xpath)
        state_option.click()

        self.fill("ID:billing_phone", self.order_to_exe['client']['customer']['phone'])

        print("Terminado el trabajo con el Checkout. ---")


    def main(self):
        try:
            if len(sys.argv) != 2:
                print("Usage: python router.py <test_file>")
                return

            test_file    = sys.argv[1]
            instructions = self.load_instructions(test_file)

            self.login_data       = instructions.get('login_data')
            self.cart_page        = instructions.get('cart_page')
            self.checkout_page    = instructions.get('checkout_page')
            self.order_to_exe     = instructions.get('order_to_exe')
            self.qty_input_number = instructions.get('qty_input_number')
            self.add_to_cart_btn  = instructions.get('add_to_cart_btn')

            # Espera implicita
            # self.driver.implicitly_wait(10)


            #
            # Login
            #
            
            self.login()

            # self.driver.maximize_window()


            #
            # Carrito
            #

            # cart_items = self.get_cart_items()
            # self.print_cart_items(cart_items)


            #
            # Orden
            #

            print("COMIENZO A EJECUTAR LA ORDEN: --->\r\n")

            for product in self.order_to_exe['products']:
                
                product_page = product['slug'] 
                quantity     = product['qty']
                attrs        = product.get('attrs', {})  # Evita errores si no hay atributos definidos

                self.nav(product_page)

                for att_name, att_value in attrs.items():
                    self.fill(att_name, att_value)

                # Llena la cantidad y agrega al carrito
                self.fill(self.qty_input_number, str(quantity), 5, False)

                self.get(self.add_to_cart_btn).click()

                time.sleep(2)  

            print("FINALIZADA LA EJECUCION DE LA ORDEN <---\r\n")

            #
            # Carrito
            #

            cart_items = self.get_cart_items()
            self.print_cart_items(cart_items)

            #
            # Checkout
            #

            self.set_checkout()

            # quiting
            self.quit(60)

        except Exception as e:
            # print("Se ha producido un error durante la ejecución:", e)
            traceback.print_exc(limit=5)

        # finally:
            

if __name__ == "__main__":
    automation = MyScraper()

    # 
    # .env
    #
    # pip install python-dotenv
    #
    # https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1
    #

    load_dotenv()

    if os.getenv('IS_PRODUCTION') == 'True':
        is_prod = True
    else:
        is_prod = False

    web_driver = os.getenv('WEB_DRIVER')


    automation.setup(is_prod, False, web_driver)
    automation.main()
