import time
import sys
import os
import re

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


class WebAutomation:
    def nav(self, slug, delay=0):
        site_url = self.login_data['site_url'].rstrip('/')
        self.driver.get(site_url + '/' + slug)

    def save_html(filename):
        """
        Salva renderizado en archivo
        """
        
        if not filename.endswith('.html'):
            filename += '.html'

        html = self.driver.page_source
        
        with open(filename, 'w') as f:
            f.write(html)

    def get(self, selector, single=True, t=10, debug=False):
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

    
    def fill(self, selector, value):
        """
        Rellena un elemento INPUT

        Funcionando con INPUT TEXT
        """
        element = self.get(selector)
        element_tag = element.tag_name

        if element_tag == 'input' or element_tag == 'textarea':
            element.clear()
            element.send_keys(value)
        elif element_tag == 'select':            
            select = Select(element)
            select.select_by_visible_text(value)
        else:
            raise ValueError(f"Unsupported element type: {element_tag}")        

    def main(self): pass


