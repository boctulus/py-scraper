#!/usr/bin/env python

import os
import time
import sys
import json
import traceback

from libs.web_automation import WebAutomation

class MyScraper(WebAutomation):
    def main(self):
        try:
            self.driver.maximize_window()
            self.driver.get('https://www.mateandoarg.com/materas/porta-mate-rutero-cuero')  # URL del producto

            with open('instructions/instructions.json', 'r') as f:
                instructions = json.load(f)

            result = self.get_json(instructions)
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