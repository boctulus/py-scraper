#!/usr/bin/env python

import os
import time
import sys
import json
import traceback

from libs.web_automation import WebAutomation

class MyScraper(WebAutomation):
    def main(self):
        # Archivo con HTML a procesar
        html_file_path = 'D:\python\selenium\py-scraper\page.html'

        # Instrucciones de qué y cómo hacer el scraping
        filename = 'instructions/instructions.json'

        try:
            with open(filename, 'r') as f:
                instructions = json.load(f)

            # Proceso desde archivo
            result_from_file = self.get_json_using_xpath_from_file(instructions, html_file_path, debug=True, fail_if_not_exist=False)
            print("Resultados desde archivo HTML:")
            print(json.dumps(result_from_file, indent=4, ensure_ascii=False))

        except Exception as e:
            print(f"Ocurrió un error no esperado: {e}")
            traceback.print_exc(limit=5)
        finally:
            self.quit(5)

if __name__ == "__main__":
    automation = MyScraper()
    automation.main()
