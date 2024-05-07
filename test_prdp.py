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

import time
import sys
import os
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


    def login(self):
        self.nav(self.login_data['login_page'], 1)

        username_input = self.driver.find_element(By.ID, 'user_login')
        username_input.send_keys(self.login_data['log'])

        password_input = self.driver.find_element(By.ID, 'user_pass')
        password_input.send_keys(self.login_data['pwd'])

        login_button = self.driver.find_element(By.ID, 'wp-submit')
        login_button.click()


    def load_instructions(self, test_file):
        instructions = {}
        test_file_path = os.path.join('instructions', test_file)
       
        if not os.path.isfile(test_file_path):
            print(f"Error: File '{test_file}' not found.")
            return

        with open(test_file_path, 'r') as f:
            exec(f.read(), instructions)
            
        return instructions


    def get(self, selector, single=True, t=10, debug=True):
        """
        Obtiene un "selector" de CSS

        Tipos soportados:

        ID = "id"
        NAME = "name"
        XPATH = "xpath"
        LINK_TEXT = "link text"
        PARTIAL_LINK_TEXT = "partial link text"
        TAG_NAME = "tag name"
        CLASS_NAME = "class name"
        CSS_SELECTOR = "css selector"

        Args:
            selector (str):         El selector del elemento, que puede comenzar con uno de los siguientes identificadores seguido
                                    de dos puntos (ID:, NAME:, XPATH:, LINK_TEXT:, PARTIAL_LINK_TEXT:, TAG_NAME:, CLASS_NAME:),
                                    seguido del valor del selector.

            debug (bool, opcional): Indica si se debe imprimir información de depuración. Por defecto es False.

        Returns:
            selenium.webdriver.remote.webelement.WebElement: El elemento encontrado en la página.

        Ejemplo de uso:
            # Buscar un elemento por su ID
            elemento = self.get('ID:my_id')

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
        elif selector.startswith('CSS_SELECTOR:'):
            locator = By.CSS_SELECTOR
            value = selector[13:]  # Ignorar las primeras catorce letras 'CSS_SELECTOR:'
        else:
            locator = By.CSS_SELECTOR
            value = selector

        if debug:
            print(f"{selector} > {value}")


        if (single):
            return WebDriverWait(self.driver, t).until(
                EC.visibility_of_element_located((locator, value))
            )
        else:
             return WebDriverWait(self.driver, t).until(
                EC.presence_of_all_elements_located((locator, value))
            )

    def get_all(self, selector, t=10, debug=False):
        return self.get(selector, single=False, t=t, debug=debug)

    def get_attr(self, selector, attr_name, t=10, debug=False):
        """
        Obtiene el valor de un atributo de un elemento identificado por un selector CSS.

        Args:
            selector (str):         Selector CSS del elemento.
            attr_name (str):        Nombre del atributo que se desea obtener.
            t (int, opcional):      Tiempo máximo de espera en segundos. Por defecto es 10 segundos.
            debug (bool, opcional): Indica si se debe imprimir información de depuración. Por defecto es False.

        Returns:
            str: El valor del atributo especificado.

        Ejemplo de uso:
            # Obtener el atributo href de un enlace
            href_value = self.get_attr('a', 'href')
        """
        element = self.get(selector, t, debug)
        return element.get_attribute(attr_name)

    def get_text(self, selector, t=10, debug=False):
        """
        Obtiene el texto contenido dentro de un elemento identificado por un selector CSS.

        Args:
            selector (str):         Selector CSS del elemento.
            t (int, opcional):      Tiempo máximo de espera en segundos. Por defecto es 10 segundos.
            debug (bool, opcional): Indica si se debe imprimir información de depuración. Por defecto es False.

        Returns:
            str: El texto contenido dentro del elemento especificado.

        Ejemplo de uso:
            # Obtener el texto de un elemento de clase 'title'
            title_text = self.get_text('.title')
        """
        element = self.get(selector, t, debug)
        return element.text    

    def main(self):
        instructions     = self.load_instructions('gourmet.py')

        self.login_data  = instructions.get('login_data')

        try:
            self.nav('/producto/queso-oregano-530gr/')

            title = self.get_text("XPATH://h1[@class='product-title product_title entry-title']")
            price = self.get_text("XPATH://div[@class='product-main']//bdi[1]")
            description = self.get_text("XPATH://div[@class='product-short-description']/p")
            stock = self.get_text("CSS_SELECTOR:p.stock.in-stock")
            sku = self.get_text("CSS_SELECTOR:span.sku")

            print("Title:", title)
            print("Price:", price)
            print("Stock:", stock)
            print("SKU:",   sku)


        finally:
            print("Esperando para salir")
            # time.sleep(60)
            
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
