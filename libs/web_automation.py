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

from selenium.common.exceptions import NoSuchElementException


class WebAutomation:
    def debug(value=True):
        self.debug = value

    def nav(self, slug, delay=0):
        site_url = self.login_data['site_url'].rstrip('/')
        url      = site_url + '/' + slug

        if self.debug:
            print(f"Navegando a '{url}'")

        self.driver.get(url)

    def quit(self, delay=0):
        time.sleep(delay)

        if self.debug:
            print(f"\r\nSaliendo...")

        self.driver.quit()
        sys.exit()

    def save_html(self, filename):
        """
        Salva renderizado en archivo
        """
        
        if not filename.endswith('.html'):
            filename += '.html'

        html = self.driver.page_source
        
        with open(filename, 'w') as f:
            f.write(html)

    def _get(self, selector, root=None, single=True, fail_if_not_exist=True, timeout=10, debug=False):
        """
        Obtiene un "selector" de CSS dentro de un elemento raíz.

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
            single (bool, opcional): Indica si se espera un solo elemento. Por defecto es True.
            root (WebElement, opcional): Elemento raíz dentro del cual buscar el selector. Por defecto es None (la página completa).
            debug (bool, opcional): Indica si se debe imprimir información de depuración. Por defecto es False.

        Returns:
            selenium.webdriver.remote.webelement.WebElement o lista de elementos: El elemento encontrado en la página, o una lista de elementos si single es False.
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

        if self.debug or debug:
            print(f"{selector} > {value}")

        try:
            if (single):
                element = WebDriverWait(root or self.driver, timeout).until(
                    EC.visibility_of_element_located((locator, value))
                )
                return element
            else:
                elements = WebDriverWait(root or self.driver, timeout).until(
                    EC.presence_of_all_elements_located((locator, value))
                )
                return elements
        except:
            if fail_if_not_exist:
                traceback.print_exc()
                raise ValueError(f"Element(s) not found: {selector}")
            else:
                if (single):
                    return False
                else:
                    return []

    def get(self, selector, root=None, fail_if_not_exist=True, timeout=10, debug=False):
        return self._get(selector, single=True, root=root, fail_if_not_exist=fail_if_not_exist, timeout=timeout, debug=debug)

    def get_all(self, selector, root=None, fail_if_not_exist=True, timeout=10, debug=False):
        return self._get(selector, single=False, root=root, fail_if_not_exist=fail_if_not_exist, timeout=timeout, debug=debug)

    def get_attr(self, selector, attr_name, root=None, fail_if_not_exist=True, timeout=10, debug=False):
        """
        Obtiene el valor de un atributo de un elemento identificado por un selector CSS dentro de un elemento raíz.

        Args:
            selector (str):         Selector CSS del elemento.
            attr_name (str):        Nombre del atributo que se desea obtener.
            root (WebElement, opcional): Elemento raíz dentro del cual buscar el selector. Por defecto es None (la página completa).
            timeout (int, opcional):      Tiempo máximo de espera en segundos. Por defecto es 10 segundos.
            debug (bool, opcional): Indica si se debe imprimir información de depuración. Por defecto es False.

        Returns:
            str: El valor del atributo especificado.
        """
        element = self.get(selector, root=root, fail_if_not_exist=fail_if_not_exist, timeout=timeout, debug=debug)
        return element.get_attribute(attr_name)

    def get_text(self, selector, root=None, fail_if_not_exist=True, timeout=10, debug=False):
        """
        Obtiene el texto contenido dentro de un elemento identificado por un selector CSS dentro de un elemento raíz.

        Args:
            selector (str):         Selector CSS del elemento.
            root (WebElement, opcional): Elemento raíz dentro del cual buscar el selector. Por defecto es None (la página completa).
            timeout (int, opcional):      Tiempo máximo de espera en segundos. Por defecto es 10 segundos.
            debug (bool, opcional): Indica si se debe imprimir información de depuración. Por defecto es False.

        Returns:
            str: El texto contenido dentro del elemento especificado.
        """
        element = self.get(selector, root=root, fail_if_not_exist=fail_if_not_exist, timeout=timeout, debug=debug)
        return element.text


    def fill(self, selector, value, root=None, fail_if_not_exist=True, timeout=5):
        """
        Rellena un elemento de formulario como INPUT TEXT, TEXTAREA y SELECT 
        (SELECT2 de momento no)

        Ej:

        self.fill('NAME:selecttalla', 'U')
        self.fill('NAME:selectcolor', 'negro')

        Si el elemento puede no existir, se debe enviar fail_if_not_exist=False.
        """

        try:
            if self.debug:
                print(f"Seteando valor {selector} > {value}")

            element = self.get(selector, root=root, fail_if_not_exist=fail_if_not_exist,timeout=timeout)

            element_tag = element.tag_name

            if element_tag == 'input' or element_tag == 'textarea':
                element.clear()
                element.send_keys(value)
            elif element_tag == 'select':            
                select = Select(element)
                select.select_by_visible_text(value)
            else:
                raise ValueError(f"Unsupported element type: {element_tag}") 

            return True

        except:
            if fail_if_not_exist:
                traceback.print_exc()
                raise ValueError(f"Element not found: {selector}")
            else:
                return False


    def load_instructions(self, test_file):
        instructions = {}
        test_file_path = os.path.join('instructions', test_file)
       
        if not os.path.isfile(test_file_path):
            print(f"Error: File '{test_file}' not found.")
            return

        with open(test_file_path, 'r') as f:
            exec(f.read(), instructions)
            
        return instructions       

    def login(self, debug = False):
        self.nav(self.login_data['login_page'])

        default_selectors = {
            'username_input':    'ID:user_login',
            'password_input':    'ID:user_pass',
            'remember_checkbox': 'NAME:rememberme',
            'submit_button':     'ID:wp-submit'
        }

        custom_selectors = self.login_data.get('selectors', default_selectors)

        # Obtener los selectores personalizados o los predeterminados
        username_selector = custom_selectors.get('username_input', default_selectors['username_input'])
        password_selector = custom_selectors.get('password_input', default_selectors['password_input'])
        submit_button     = custom_selectors.get('submit_button',  default_selectors['submit_button'])

        if debug:
            print('username_selector: ' + username_selector) 
            print('password_selector: ' + password_selector)
            print('submit_button: '     + submit_button)

        # Enviar las credenciales al formulario de inicio de sesión
        username_input = self.get(username_selector)
        username_input.send_keys(self.login_data['log'])

        password_input = self.get(password_selector)
        password_input.send_keys(self.login_data['pwd'])

        # Hacer clic en el botón de inicio de sesión
        login_button = self.get(submit_button)
        login_button.click()


    def main(self): pass


