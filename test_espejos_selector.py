#!/usr/bin/env python

import os
import time
import sys
import re
import traceback

import undetected_chromedriver as uc

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from dotenv import load_dotenv

from libs.web_automation import WebAutomation
from libs.instruction_loader import InstructionLoader
from libs.label import Label
from libs.files import Files
from libs.dataobject import DataObject

import shutil
import logging
from logging.handlers import RotatingFileHandler


class MyScraper(WebAutomation):
    """
        https://chatgpt.com/c/b460b582-3f19-48e4-bd76-ae1f5c322890
    """
    
    def __init__(self):
        self.driver = None
        self.debug  = True

    def sleep(self, t: int):
        logging.debug(f"Taking a nap for {t} seconds ...zzzz...") #
        time.sleep(t)

    class Product: 
        @staticmethod
        def print(self):
            print("Title:", self.title)
            print("Price:", self.price)
            print("Avail:", self.avail)
            # print("SKU:",   self.sku)
            print("--------------------------------------\r\n")

    '''
        La idea...... 
        
        nav_to_variation() -> get_product()
    '''

    def get_product(self, data):
        if data.product_url is not None:
            self.nav(data.product_url)

        time.sleep(10)

        self.select_every_selector_by_attributes(data.attrs)

        p = self.Product()

        p.title = self.get_text("XPATH://h1[@itemprop='name']", fail_if_not_exist=False)
        p.price = self.get_text("XPATH://div[@class='Price']//span[@class='price-value']//span[@itemprop='price']", fail_if_not_exist=False)
        p.avail = self.exists("XPATH://p[contains(text(), 'En existencias')]", fail_if_not_exist=False)
        p.var_url = self.driver.current_url

        return p

    def wait_until_elements_present(self, selector, timeout=10):
        """
        Espera hasta que al menos un elemento identificado por el selector esté presente en la página.
        """
        self.get(selector, timeout=timeout)
   
    def main(self):
        try:
            '''
            Algo asi pasaria como JSON via linea de comandos
            '''
            instructions = {
                "data": {
                    "product_url": "https://www.azulejosmadridonline.es/epages/63993920.sf/es_ES/?ObjectPath=/Shops/63993920/Products/stcne",
                    "attrs": [
                        {
                            "Ancho": "70",
                            "Largo": "70",
                            "Textura": "Pizarra",
                            "Rejilla": "Rejilla Inox."
                        }
                    ]
                }
            }
            
            if instructions is None:
                print("Failed to load instructions.")
                return

            ins_dict = instructions.get('data')

            # Convertir el diccionario en un objeto
            data = DataObject(**ins_dict)


            """
            Ajustes al web driver
            """

            # self.driver.implicitly_wait(10)
            self.driver.maximize_window()


            """
            Scraping de producto
            """

            # attrs = data.attrs    

            # self.nav(data.product_url)
            # self.sleep(5)
            # self.wait_until_elements_present(att_selector)
            # self.fill(att_selector, att_value)

            p = self.get_product(data)
            self.Product.print(p)

            # quiting
            if not self.is_prod:
                self.quit(6000)

        except Exception as e:
            # print("Se ha producido un error durante la ejecución:", e)
            traceback.print_exc(limit=5)


        finally:
            if not self.is_prod:
                self.quit(5000)
            

if __name__ == "__main__":    
    automation = MyScraper()

    load_dotenv()

    automation.is_prod  = (os.getenv('IS_PRODUCTION') == 'True')
    automation.headless = automation.is_prod or (os.getenv('OPT_HEADLESS') == 'True')

    web_driver = os.getenv('WEB_DRIVER')

    automation.setup(automation.headless, False, web_driver)
    automation.main()
