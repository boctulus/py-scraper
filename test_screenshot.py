#!/usr/bin/env python

import time
import sys
import os
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

from libs.select2 import Select2


class MyScraper(WebAutomation):
    """
        https://chatgpt.com/c/b460b582-3f19-48e4-bd76-ae1f5c322890
    """
    
    def __init__(self):
        self.driver = None
        self.debug  = True

    def main(self):
        try:
            self.driver.maximize_window()
            self.nav('https://www.python.org')
            
            self.take_screenshot('mi_archivo3.png')

        except Exception as e:
            traceback.print_exc(limit=5)
        finally:
            self.quit(60)

if __name__ == "__main__":
    automation = MyScraper()
    automation.setup(True, False, 'Google')
    automation.main()
