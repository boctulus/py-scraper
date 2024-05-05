import time
import sys
import os
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.firefox.options import Options as FireFoxOptions
from selenium.webdriver.firefox.service import Service as FireFoxService
from webdriver_manager.firefox import DriverManager as FireFoxDriverManager
from dotenv import load_dotenv

class WebAutomation:
    def __init__(self):
        self.driver = None

    def nav(self, slug, delay=0):
        site_url = self.login_data['site_url'].rstrip('/')
        self.driver.get(site_url + '/' + slug)
        time.sleep(delay)


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


    def get_selector(self, selector, debug=False):
        """
        Busca un elemento en la página web utilizando diferentes tipos de selectores.

        Args:
            selector (str):         El selector del elemento, que puede comenzar con uno de los siguientes identificadores seguido
                                    de dos puntos (ID:, NAME:, XPATH:, LINK_TEXT:, PARTIAL_LINK_TEXT:, TAG_NAME:, CLASS_NAME:),
                                    seguido del valor del selector.

            debug (bool, opcional): Indica si se debe imprimir información de depuración. Por defecto es False.

        Returns:
            selenium.webdriver.remote.webelement.WebElement: El elemento encontrado en la página.

        Ejemplo de uso:
            # Buscar un elemento por su ID
            elemento = self.get_selector('ID:my_id')

            ID = "id"
            NAME = "name"
            XPATH = "xpath"
            LINK_TEXT = "link text"
            PARTIAL_LINK_TEXT = "partial link text"
            TAG_NAME = "tag name"
            CLASS_NAME = "class name"
            CSS_SELECTOR = "css selector"

            https://selenium-python.readthedocs.io/locating-elements.html
        """

        if selector.startswith('ID:'):
            locator = By.ID
            value = selector[3:]  # Ignorar las primeras tres letras 'ID:'
        elif selector.startswith('NAME:'):
            locator = By.NAME
            value = selector[5:]  # Ignorar las primeras cinco letras 'NAME:'
        elif selector.startswith('XPATH:'):
            locator = By.XPATH
            value = selector[6:]  # Ignorar las primeras seis letras 'XPATH:'
        elif selector.startswith('LINK_TEXT:'):
            locator = By.LINK_TEXT
            value = selector[10:]  # Ignorar las primeras diez letras 'LINK_TEXT:'
        elif selector.startswith('PARTIAL_LINK_TEXT:'):
            locator = By.PARTIAL_LINK_TEXT
            value = selector[18:]  # Ignorar las primeras dieciocho letras 'PARTIAL_LINK_TEXT:'
        elif selector.startswith('TAG_NAME:'):
            locator = By.TAG_NAME
            value = selector[9:]  # Ignorar las primeras nueve letras 'TAG_NAME:'
        elif selector.startswith('CLASS_NAME:'):
            locator = By.CLASS_NAME
            value = selector[11:]  # Ignorar las primeras once letras 'CLASS_NAME:'
        else:
            locator = By.CSS_SELECTOR
            value = selector

        if debug:
            print(f"{selector} > {value}")

        return self.driver.find_element(locator, value)


    def login(self, debug = False):
        self.nav(self.login_data['login_page'])

        default_css_selectors = {
            'username_input':    'ID:user_login',
            'password_input':    'ID:user_pass',
            'remember_checkbox': 'NAME:rememberme',
            'submit_button':     'ID:wp-submit'
        }

        custom_selectors = self.login_data.get('css_selectors', default_css_selectors)

        # Obtener los selectores personalizados o los predeterminados
        username_selector = custom_selectors.get('username_input', default_css_selectors['username_input'])
        password_selector = custom_selectors.get('password_input', default_css_selectors['password_input'])
        submit_button     = custom_selectors.get('submit_button',  default_css_selectors['submit_button'])

        if debug:
            print('username_selector: ' + username_selector) 
            print('password_selector: ' + password_selector)
            print('submit_button: '     + submit_button)

        # Enviar las credenciales al formulario de inicio de sesión
        username_input = self.get_selector(username_selector)
        username_input.send_keys(self.login_data['log'])

        password_input = self.get_selector(password_selector)
        password_input.send_keys(self.login_data['pwd'])

        # Hacer clic en el botón de inicio de sesión
        login_button = self.get_selector(submit_button)
        login_button.click()


    def get_cart_items(self):
        self.nav(self.cart_page)

        cart_items = []

        product_rows = WebDriverWait(self.driver, 10).until(
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

        title_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h1[@class='product-title product_title entry-title']"))
        )
        p.title = title_element.text


        price_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='product-main']//bdi[1]"))
        )
        p.price = price_element.text

        description_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='product-short-description']/p"))
        )
        p.description = description_element.text

        stock_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "p.stock.in-stock"))
        )
        p.stock = stock_element.text

        sku_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span.sku"))
        )
        p.sku = sku_element.text

        # Retorna un objeto Producto
        return p

    def load_instructions(self, test_file):
        instructions = {}
        test_file_path = os.path.join('instructions', test_file)
       
        if not os.path.isfile(test_file_path):
            print(f"Error: File '{test_file}' not found.")
            return

        with open(test_file_path, 'r') as f:
            exec(f.read(), instructions)
            
        return instructions

    def set_checkout(self):
        self.nav(self.checkout_page)

         # Establecer el nombre
        billing_first_name_input = self.driver.find_element(By.XPATH, "//input[@id='billing_first_name']")
        billing_first_name_input.clear()
        billing_first_name_input.send_keys(self.order_to_exe['client']['shipping_addr']['billing_first_name'])

        # Establecer el apellido
        billing_last_name_input = self.driver.find_element(By.XPATH, "//input[@id='billing_last_name']")
        billing_last_name_input.clear()
        billing_last_name_input.send_keys(self.order_to_exe['client']['shipping_addr']['billing_last_name'])

        # Establecer la dirección de facturación

        billing_address_1_input = self.driver.find_element(By.ID, 'billing_address_1')
        billing_address_1_input.clear()
        billing_address_1_input.send_keys(self.order_to_exe['client']['shipping_addr']['billing_address_1'])

        billing_address_2_input = self.driver.find_element(By.ID, 'billing_address_2')
        billing_address_2_input.clear()
        billing_address_2_input.send_keys(self.order_to_exe['client']['shipping_addr']['billing_address_2'])

        billing_city_input = self.driver.find_element(By.ID, 'billing_city')
        billing_city_input.clear()
        billing_city_input.send_keys(self.order_to_exe['client']['shipping_addr']['billing_city'])

        billing_postcode_input = self.driver.find_element(By.ID, 'billing_postcode')
        billing_postcode_input.clear()
        billing_postcode_input.send_keys(self.order_to_exe['client']['shipping_addr']['billing_postcode'])

        # Seleccionar el estado de facturación
        billing_state_input = self.driver.find_element(By.ID, 'select2-billing_state-container')
        billing_state_input.click()
        state_option_xpath = f"//ul[@id='select2-billing_state-results']//li[contains(text(), '{self.order_to_exe['client']['shipping_addr']['billing_state']}')]"
        state_option = self.driver.find_element(By.XPATH, state_option_xpath)
        state_option.click()

        # Establecer el teléfono
        billing_phone_input = self.driver.find_element(By.ID, 'billing_phone')
        billing_phone_input.clear()
        billing_phone_input.send_keys(self.order_to_exe['client']['customer']['phone'])

        # Agregar notas al pedido
        order_comments_input = self.driver.find_element(By.ID, 'order_comments')
        order_comments_input.clear()
        order_comments_input.send_keys(self.order_to_exe['order_comments'])


    def main(self):
        if len(sys.argv) != 2:
            print("Usage: python router.py <test_file>")
            return

        test_file = sys.argv[1]
        instructions = self.load_instructions(test_file)

        self.login_data    = instructions.get('login_data')
        self.cart_page     = instructions.get('cart_page')
        self.checkout_page = instructions.get('checkout_page')
        self.order_to_exe  = instructions.get('order_to_exe')

        try:
            #
            # Login
            #
            
            self.login()

            self.driver.maximize_window()

            #
            # Carrito
            #

            cart_items = self.get_cart_items()
            self.print_cart_items(cart_items)


            #
            # Orden
            #

            print("COMIENZO A EJECUTAR LA ORDEN: --->\r\n")
            for products in self.order_to_exe['products']:
                product_page = products['prd']
                quantity     = products['qty']

                self.nav(product_page, 2)

                p = self.get_product(product_page)
                self.Product.print(p)

                quantity_input = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.quantity.buttons_added input[type='number'][name='quantity']"))
                )

                quantity_input.clear()
                quantity_input.send_keys(str(quantity))

                add_to_cart_button = self.driver.find_element(By.CSS_SELECTOR, "button.single_add_to_cart_button")
                add_to_cart_button.click()
                time.sleep(3)
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


        finally:
            time.sleep(60)
            self.driver.quit()


if __name__ == "__main__":
    automation = WebAutomation()

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
