import time
import sys
import os
import re
import traceback
import json

import undetected_chromedriver as uc

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.firefox.options import Options as FireFoxOptions
from selenium.webdriver.firefox.service import Service as FireFoxService
from webdriver_manager.firefox import DriverManager as FireFoxDriverManager

from lxml import etree, html

import shutil
import logging
from logging.handlers import RotatingFileHandler

"""
    https://claude.ai/chat/a3452697-a1bc-4b24-8606-62dfc0d4dd08
    https://chatgpt.com/c/b460b582-3f19-48e4-bd76-ae1f5c322890

    Instalacion

    pip install lxml

    Cache

    https://chatgpt.com/c/35523ed3-9ffb-46c3-8cec-606eb32a34b1
"""
class WebAutomation:
    def set_base_url(self, url):
        self.base_url = url.rstrip('/')

    def debug(self, value=True):
        self.debug = value

    def nav(self, url, debug=False):    
        if debug or self.debug:
            print(f"Navegando a '{url}'")

        self.driver.get(url)

    def nav_slug(self, slug, debug=False):        
        url = self.base_url + '/' + slug
        self.nav(url)

    def quit(self, delay=0):
        if not self.headless:
            time.sleep(delay)

        if self.debug:
            print("\r\nSaliendo...")

        if self.driver is not None:
            self.driver.quit()
        
        sys.exit()

    def save_html(self, filename, encoding='utf-8', debug=False):
        """
        Salva renderizado en archivo
        """
        
        if not filename.endswith('.html'):
            filename += '.html'

        html = self.driver.page_source

        if self.debug or debug:
            print(f'Filename: {filename}\n')
            print(html)
        
        try:
            if encoding is None:
                encoding = 'utf-8'

            with open(filename, 'w', encoding=encoding) as f:
                f.write(html)
        except Exception as e:
            print(f"Error al escribir el archivo '{filename}': {e}")


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
            selector (str): el selector del elemento, que puede comenzar con uno de los siguientes identificadores seguido
                            de dos puntos (ID:, NAME:, XPATH:, LINK_TEXT:, PARTIAL_LINK_TEXT:, TAG_NAME:, CLASS_NAME:),
                            seguido del valor del selector.
            
            single (bool, opcional): indica si se espera un solo elemento. Por defecto es True.
            
            root (WebElement, opcional): elemento raíz dentro del cual buscar el selector. Por defecto es None (la página completa).
            
            debug (bool, opcional): endica si se debe imprimir información de depuración. Por defecto es False.

        Returns:
            selenium.webdriver.remote.webelement.WebElement o lista de elementos: el elemento encontrado en la página, o una lista de elementos si single es False.
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
            print(f'Selector: {selector} ; single: {single}')

        try:
            if (single):
                element = WebDriverWait(root or self.driver, timeout).until(
                    # EC.element_to_be_clickable
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

    def exists(self, selector, root=None, single=True, fail_if_not_exist=True, timeout=10, debug=False):
        ret = self._get(selector, single=True, root=root, fail_if_not_exist=fail_if_not_exist, timeout=timeout, debug=debug)

        if single:
            return ret is not False and ret is not None
        else:
            return len(ret) > 0

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

    # ok
    def get_attr_all(self, selector, attr_name, root=None, fail_if_not_exist=True, timeout=10, debug=False):
        """ 
        Ej:

        self.driver.maximize_window()
        self.nav('https://www.mateandoarg.com/materas/porta-mate-rutero-cuero')
        
        xpath_selector = "//div[contains(@class, 'product-vip__images-grid')]//ul[contains(@class, 'product-vip__images-grid-list')]//li[contains(@class, 'product-vip__images-grid-list-item')]//img"

        print(self.get_attr_all('XPATH:' + xpath_selector, 'src'))
        """
        elements = self.get_all(selector, root=root, fail_if_not_exist=fail_if_not_exist, timeout=timeout, debug=debug)
        return [element.get_attribute(attr_name) for element in elements]

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

    def get_text_all(self, selector, root=None, fail_if_not_exist=True, timeout=10, debug=False):
        """
        Obtiene el texto contenido dentro de una lista de elementos identificados por un selector CSS dentro de un elemento raíz.

        Args:
            selector (str): Selector CSS del elemento.
            root (WebElement, opcional): Elemento raíz dentro del cual buscar el selector. Por defecto es None (la página completa).
            fail_if_not_exist (bool, opcional): Indica si debe fallar si no se encuentra ningún elemento. Por defecto es True.
            timeout (int, opcional): Tiempo máximo de espera en segundos. Por defecto es 10 segundos.
            debug (bool, opcional): Indica si se debe imprimir información de depuración. Por defecto es False.

        Returns:
            list: Lista de textos contenidos dentro de los elementos especificados.
        """
        elements = self.get_all(selector, root=root, fail_if_not_exist=fail_if_not_exist, timeout=timeout, debug=debug)
        return [element.text.strip() for element in elements] if elements else []


    def clean_text(self, text):
        return re.sub(r'\s+', ' ', text).strip()

    def evaluate(self, selector, return_all=False, attribute=None, root=None, fail_if_not_exist=True, timeout=10, debug=False):
        """
        Evalúa un selector CSS y obtiene los atributos o textos de los elementos seleccionados.

        Args:
            selector (str): El selector CSS del elemento.
            return_all (bool, opcional): Indica si se deben devolver todos los elementos encontrados. Por defecto es False.
            attribute (str, opcional): El atributo que se desea obtener. Si es None, se devuelve el texto del elemento.

        Returns:
            str, list o None: El texto o atributo del primer elemento encontrado si return_all es False,
                            o una lista de textos o atributos de todos los elementos encontrados si return_all es True.
        """
        if return_all:
            elements = self.get_all(selector, root, fail_if_not_exist, timeout, debug)
            if attribute:
                return [element.get_attribute(attribute) for element in elements] if elements else None
            else:
                return [element.text.strip() for element in elements] if elements else None
        else:
            element = self.get(selector)
            if attribute:
                return element.get_attribute(attribute) if element else None
            else:
                return element.text.strip() if element else None

    def evaluate_xpath(self, selector, return_all=False, attribute=None, root=None, fail_if_not_exist=True, timeout=10, debug=False):
        """
        Evalúa un selector XPath y obtiene los atributos o textos de los elementos seleccionados.

        Similar a evaluate() pero actúa solo sobre selectores XPath.
        """
        if not selector.startswith('XPATH:'):
            selector = f"XPATH:{selector}"

        return self.evaluate(selector, return_all, attribute, root, fail_if_not_exist, timeout, debug)

    def get_json(self, instructions, fail_if_not_exist=True, timeout=10, debug=False):
        """
        Obtiene contenido o atributos de cada selector CSS de un JSON.

        Ejemplo:

        {
            "nombre_producto": "XPATH://h1",
            "precio_original": "XPATH://p/span/del",
            "precio_descuento": "XPATH://span[@class='product-vip__price-value']", 
            "porcentaje_descuento": "XPATH://span[@class='product-vip__off-value']",
            "cuotas_sin_interes": {
                "numero_cuotas": "XPATH://p/i/following-sibling::span/strong[1]",
                "monto_cuota": "XPATH://p/i/following-sibling::span/strong[2]"
            },
            "colores_disponibles:all": "XPATH://select[@id='atributos-0']/option",
            "imagenes:all[src]": "XPATH://div[contains(@class, 'product-vip__images-grid')]//ul[contains(@class, 'product-vip__images-grid-list')]//li[contains(@class, 'product-vip__images-grid-list-item')]//img"
        }
        """
        result = {}
        for key, value in instructions.items():
            return_all = False
            attribute = None

            # Check if the field name ends with ":all"
            if key.endswith(":all"):
                return_all = True
                key = key[:-4]  # Remove ":all" from the field name

            # Check if the field name contains an attribute
            attr_match = re.search(r'\[(\w+)\]$', key)
            if attr_match:
                attribute = attr_match.group(1)
                key = re.sub(r'\[\w+\]$', '', key)  # Remove the attribute from the field name

                # Check if the field name ends with ":all"
                if key.endswith(":all"):
                    return_all = True
                    key = key[:-4]  # Remove ":all" from the field name

            if isinstance(value, str):
                result[key] = self.evaluate(value, return_all, attribute, fail_if_not_exist=fail_if_not_exist, timeout=timeout, debug=debug)
            elif isinstance(value, dict):
                result[key] = self.get_json(value, fail_if_not_exist=fail_if_not_exist, timeout=timeout, debug=debug)

        return result

    def get_json_using_xpath(self, instructions, fail_if_not_exist=True, timeout=10, debug=False):
        """
        Similar a get_json() con la diferencia de que asume que los selectores recibidos son siempre de tipo XPath.

        De no comenzar con 'XPATH:', es agregado

        Ejemplo:

        {
            "nombre_producto": "//h1",
            "precio_original": "//p/span/del",
            "precio_descuento": "//span[@class='product-vip__price-value']", 
            "porcentaje_descuento": "//span[@class='product-vip__off-value']",
            "cuotas_sin_interes": {
                "numero_cuotas": "//p/i/following-sibling::span/strong[1]",
                "monto_cuota": "//p/i/following-sibling::span/strong[2]"
            },
            "colores_disponibles:all": "//select[@id='atributos-0']/option",
            "imagenes:all[src]": "//div[contains(@class, 'product-vip__images-grid')]//ul[contains(@class, 'product-vip__images-grid-list')]//li[contains(@class, 'product-vip__images-grid-list-item')]//img"
        }
        """
        result = {}
        for key, value in instructions.items():
            return_all = False
            attribute = None

            # Check if the field name ends with ":all"
            if key.endswith(":all"):
                return_all = True
                key = key[:-4]  # Remove ":all" from the field name

            # Check if the field name contains an attribute
            attr_match = re.search(r'\[(\w+)\]$', key)
            if attr_match:
                attribute = attr_match.group(1)
                key = re.sub(r'\[\w+\]$', '', key)  # Remove the attribute from the field name

                # Check if the field name ends with ":all"
                if key.endswith(":all"):
                    return_all = True
                    key = key[:-4]  # Remove ":all" from the field name

            if isinstance(value, str):
                result[key] = self.evaluate_xpath(value, return_all, attribute, fail_if_not_exist=fail_if_not_exist, timeout=timeout, debug=debug)
            elif isinstance(value, dict):
                result[key] = self.get_json_using_xpath(value, fail_if_not_exist=fail_if_not_exist, timeout=timeout, debug=debug)

        return result

        
    def get_input_by_value(self, value, fail_if_not_exist=True, timeout=10, debug=False):
        """
        Caso de uso: "radio buttons", otros

        Ej:

        self.get_input_by_value("flat_rate:7").click()
        """

        xpath = f'//input[@value="{value}"]'
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            return element
        except Exception as e:
            if fail_if_not_exist:
                raise ValueError(f"Element not found: {xpath}")
            else:
                return None

    def get_input_by_label_text(self, text, fail_if_not_exist=True, timeout=10, debug=False):
        """
        Caso de uso: "radio buttons", otros

        EJ:

        self.get_input_by_label_text("Recogida local").click()
        """

        # Encuentra el label que contiene el texto especificado
        label = self.get(f'XPATH://label[contains(text(), "{text}")]')

        if label is None:
            if fail_if_not_exist:
                raise ValueError(f"Label not found with text: {text}")
            else:
                return None

        # Obtén el atributo 'for' del label para encontrar el input asociado
        radio_button_id = label.get_attribute('for')

        # Encuentra el input usando el id obtenido y haz clic en él
        radio_button = self.get(f'ID:{radio_button_id}')
        
        return radio_button

    # Hacer clic usando JavaScript
    def click_by_js(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    def click_selector(self, selector):
        element = self.get(selector)

        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            self.driver.execute_script("arguments[0].click();", element)

    def send_return(self, element, value):
        """
        I was able to get around it by using .SendKeys(Keys.Return) instead of .Click. 
         
        This worked for me in Chrome where I was having this issue and in Firefox where I was having another similar issue on this particular link
        (anchor wrapped in a Div)
        """
        element.send_keys(value)

    def fill(self, selector, value, root=None, fail_if_not_exist=True, scrollToView=False, timeout=5):
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

            if scrollToView:
                # Desplazar el elemento a la vista
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

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

    def load_instructions_from_python(self, filename):
        instructions = {}
        filename_path = os.path.join('instructions', filename)
       
        if not os.path.isfile(filename_path):
            print(f"Error: File '{filename}' not found.")
            return

        with open(filename_path, 'r') as f:
            exec(f.read(), instructions)
            
        return instructions  

    def load_instructions_from_json(self, json_file):
        json_file_path = os.path.join('instructions', json_file)
        
        if not os.path.isfile(json_file_path):
            print(f"Error: File '{json_file}' not found.")
            return

        try:
            with open(json_file_path, 'r') as f:
                data = f.read()
                if not data:
                    print(f"Error: File '{json_file}' is empty.")
                    return
                instructions = json.loads(data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file '{json_file}': {e}")
            return
        except Exception as e:
            print(f"Unexpected error reading file '{json_file}': {e}")
            return
        
        return instructions   

    def load_instructions(self, file_name):
        if file_name.endswith('.json'):
            return self.load_instructions_from_json_string(file_name)
        else:
            return self.load_instructions_from_python(file_name) 

    def login(self, slug, selectors, username, password, debug = False):
        self.nav_slug(slug)

        # Obtener los selectores personalizados o los predeterminados
        username_selector = selectors.get('username_input')
        password_selector = selectors.get('password_input')
        submit_button     = selectors.get('submit_button')

        if debug:
            print('username_selector: ' + username_selector) 
            print('password_selector: ' + password_selector)
            print('submit_button: '     + submit_button)

        # Enviar las credenciales al formulario de inicio de sesión
        username_input = self.get(username_selector)
        username_input.send_keys(username)

        password_input = self.get(password_selector)
        password_input.send_keys(password)

        # Hacer clic en el botón de inicio de sesión
        login_button = self.get(submit_button)
        login_button.click()


    def cloudflareChallenge(self):
        """
            https://stackoverflow.com/questions/76575298/how-to-click-on-verify-you-are-human-checkbox-challenge-by-cloudflare-using-se
            https://stackoverflow.com/questions/68289474/selenium-headless-how-to-bypass-cloudflare-detection-using-selenium
            https://stackoverflow.com/questions/71518406/how-to-bypass-cloudflare-browser-checking-selenium-python
            https://stackoverflow.com/questions/71518406/how-to-bypass-cloudflare-browser-checking-selenium-python
        """
        time.sleep(5)
        WebDriverWait(self.driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='Widget containing a Cloudflare security challenge']")))
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label.ctp-checkbox-label"))).click()
    
    def setup(self, headless=False, install=False, web_driver='Google'):
        """
        Este metodo no es del todo general sino que esta ajustado cargando la extension "DarkReader.crx"
        cuando headless es False

        Lo ideal seria dejar la version minima y luego agregar funcionalidad al extender la clase
        o cargar algun tipo de Trait 
        """

        self.headless = headless

        options = ChromeOptions() if web_driver == 'Google' else FireFoxOptions() if web_driver == 'FireFox' else None

        if options is None:
            raise ValueError(f"Unsupported web driver: {web_driver}. Supported options are 'Chrome' and 'Firefox'")
        
        # typically in production
        if headless:
            options.add_argument('--headless=new')
        else:
            options.add_extension("DarkReader.crx")    

        # options.add_argument("--headless")
        # options.add_argument('--headless=new')
        options.add_argument("start-maximized")
        # options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
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

    def take_screenshot(self, filename: str, full_page: bool = False, timeout: int = 1, path='screenshots/'):
        """
        Tomar screenshots en full page requiere de modo "headless" y setear el tamano de la ventana

        https://dev.to/shadow_b/capturing-full-webpage-screenshots-with-selenium-in-python-a-step-by-step-guide-187f
        """

        time.sleep(timeout)
        if not filename.endswith(".png"):
            filename += ".png"

        if full_page == False:
            self.driver.get_screenshot_as_file(f"{path}{filename}")
            return
        
        # Use JavaScript to get the full width and height of the webpage
        width  = self.driver.execute_script("return Math.max( document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth );")
        height = self.driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")

        # Set the window size to match the entire webpage
        self.driver.set_window_size(width, height)

        # Capture the screenshot of the entire page
        self.driver.get_screenshot_as_file(f"screenshots/{filename}")

    def evaluate_from_file(self, html_file_path, xpath, return_all=False, attribute=None, fail_if_not_exist=True, timeout=10, debug=False):
        with open(html_file_path, 'rb') as f:
            html_content = f.read()

        tree = etree.HTML(html_content)
        elements = tree.xpath(xpath)

        if debug:
            print(f"Selector: {xpath} ; multiple: {return_all}")

        if return_all:
            if attribute:
                return [elem.get(attribute).strip() if elem.get(attribute) else None for elem in elements]
            else:
                return [elem.text.strip() if elem.text else None for elem in elements]

        if elements:
            element = elements[0]
            if attribute:
                return element.get(attribute).strip() if element.get(attribute) else None
            else:
                return element.text.strip() if element.text else None
        else:
            if fail_if_not_exist:
                raise Exception(f"Elemento no encontrado para el selector: {xpath}")
            return None

    '''
    Similar a  get_json_using_xpath() pero desde archivo

    Experimental 
    
    No funciona para todos los selectores.
    '''
    def get_json_using_xpath_from_file(self, instructions, html_file_path, debug=False, fail_if_not_exist=True, timeout=10):
        result = {}

        for key, value in instructions.items():
            return_all = False
            attribute = None

            if ":all" in key:
                key = key.replace(":all", "")
                return_all = True
            if ":" in key:
                key, attribute = key.split(":", 1)

            if isinstance(value, dict):
                result[key] = self.get_json_using_xpath_from_file(value, html_file_path, debug, fail_if_not_exist, timeout)
            else:
                result[key] = self.evaluate_from_file(html_file_path, value, return_all, attribute, fail_if_not_exist, timeout, debug)

        return result


    ### SELECT
   
    """
    Encuentra el NAME del SELECT basándose en el texto del label asociado.
    
    :param label_text: El texto del label que estamos buscando (por ejemplo, "Ancho").
    :return: El NAME del SELECT asociado o None si no se encuentra.
    """
    def find_select_name_by_label(self, label_text):
        try:
            label = self.driver.find_element(By.XPATH, f"//label[contains(text(), '{label_text}')]")
            select_id = label.get_attribute('for')
            if select_id:
                select = self.driver.find_element(By.ID, select_id)
                return select.get_attribute('name'), select_id
            else:
                logging.warning(f"No se encontró un SELECT asociado al label '{label_text}'")
                return None, None
        except NoSuchElementException:
            logging.warning(f"No se encontró un label con el texto '{label_text}'")
            return None, None


    """
    Selecciona en cada SELECT dado su selector:valor

        {
            "NAME:SelectedVariation": "120x45x60 Dos muebles.",
            // otros
        }

        La limitacion de esta implementacion es que el NAME se puede repetir y si se se repitiera
        entre varios SELECT y para peor un campo es "Ancho" y otro es "Alto" y los valores de las dimensiones
        como puede ser 70,80,90,... se repiten tambien entre SELECT-OPTIONs el resultado seria errado.
    """

    def select_every_selector(self, attrs_list):
        for attr_name, attr_value in attrs_list.items():
            self.wait_until_elements_present(att_selector)
            self.fill(att_selector, att_value)
            self.sleep(1)

    """
    Selecciona en cada SELECT dado el nombre del campo referido desde un <LABEL for=""> y su valor

        Ej:

        {
            "Ancho": "70",
            "Largo": "70",
            "Textura": "Pizarra",
            "Rejilla": "Rejilla Inox."
        }
        
        donde el HTML puede ser algo como:

        <th class="AlignLeft MediumColumn"><label class="SelectLabelling" for="SelectedVariation0">Ancho</label></th> <!-- label -->        
        <td class="AlignLeft">
          <select name="SelectedVariation" id="SelectedVariation0" class="LongText ep-js ep-uiInput ep-uiInput-select ep-uiValidate" data-js="" data-attributeid="97325407">
            <option value="97325417" selected="selected">70</option>
            <option value="97325422">80</option>
            <option value="97325427">90</option>
          </select>
        </td>
    """
    def select_every_selector_using_labels(self, attrs_list): 
        for attr_name, attr_value in attrs_list.items():
            select_name, select_id = self.find_select_name_by_label(attr_name)
            if select_id:
                select_selector = f"ID:{select_id}"
                self.wait_until_elements_present(select_selector)
                
                # Obtener las opciones disponibles
                select_element = self.get(select_selector)
                select = Select(select_element)
                options = [option.text.strip() for option in select.options]
                
                logging.info(f"Options for {attr_name}: {options}")
                
                if attr_value in options:
                    self.fill(select_selector, attr_value)
                else:
                    logging.warning(f"Valor '{attr_value}' no encontrado para el atributo '{attr_name}'. Opciones disponibles: {options}")
                self.sleep(1)
            else:
                logging.warning(f"No se pudo encontrar un SELECT para el atributo '{attr_name}'")


    def __init__(self):
        self.test_file = None
        self.headless  = None
        self.driver    = None



    def main(self): pass