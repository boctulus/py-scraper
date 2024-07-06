#!/usr/bin/env python

import os
import time
import sys
import json
import traceback

from libs.web_automation import WebAutomation

class MyScraper(WebAutomation):
    def main(self):
        # URL a scrapear
        url      = 'https://www.mateandoarg.com/materas/porta-mate-rutero-cuero'

        # Instrucciones de que y como hacer el scraping
        filename = 'instructions/instructions.json'

        try:
            self.driver.maximize_window()
            self.driver.get(url)  

            with open(filename, 'r') as f:
                instructions = json.load(f)

            # proceso
            result = self.get_json_using_xpath(instructions, debug=True, fail_if_not_exist=False) 

            # imprimo
            print(json.dumps(result, indent=4, ensure_ascii=False))
            
        except InvalidSelectorException as e:
                print(f"Error de selector inválido: {e}")
        except TimeoutException as e:
            print(f"Tiempo de espera agotado al buscar el elemento: {e}")
        except Exception as e:
            print(f"Ocurrió un error no esperado: {e}")
            traceback.print_exc(limit=5)
        finally:
            self.quit(5)


if __name__ == "__main__":
    automation = MyScraper()
    automation.setup(True, False, 'Google')
    automation.main()