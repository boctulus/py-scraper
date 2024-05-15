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
from libs.instruction_loader import InstructionLoader
from libs.select2 import Select2
from libs.label import Label


class MyScraper(WebAutomation):
    """
        https://chatgpt.com/c/b460b582-3f19-48e4-bd76-ae1f5c322890
    """
    
    def __init__(self):
        self.driver = None
        self.debug  = True ###

    def get_cart_items(self):
        self.nav(self.data['cart']['cart_page'])

        cart_items = []

        product_rows = self.get_all("tr.woocommerce-cart-form__cart-item", fail_if_not_exist=False) # aqui

        if isinstance(product_rows, list):
            for row in product_rows:
                product_name     = self.get_text("td.product-name a", root=row)
                product_url      = self.get_attr("td.product-name a", "href", root=row)
                product_price    = self.get_text("td.product-price span.woocommerce-Price-amount", root=row)
                product_quantity = self.get_attr("td.product-quantity input.input-text.qty.text", "value", root=row)
                product_subtotal = self.get_text("td.product-subtotal span.woocommerce-Price-amount", root=row)

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

        p.title       = self.get_text("XPATH://h1[@class='product_title entry-title']")
        p.price       = self.get_text("XPATH://div[@class='product-main']//bdi[1]")
        p.description = self.get_text("XPATH://div[@class='product-short-description']/p")
        p.stock       = self.get_text("CSS_SELECTOR:p.stock.in-stock")
        p.sku         = self.get_text("CSS_SELECTOR:span.sku")

        # Retorna un objeto Producto
        return p

    def process_order(self):
        print("COMIENZO A EJECUTAR LA ORDEN: --->\r\n")

        for product in self.data['products']:
            
            product_page = product['slug'] 
            quantity     = product['qty']
            attrs        = product.get('attrs', {})  # Evita errores si no hay atributos definidos

            self.nav(product_page)

            for att_name, att_value in attrs.items():
                self.fill(att_name, att_value, fail_if_not_exist=False)

            # Llena la cantidad y agrega al carrito
            self.fill(selector=self.data['product_page']['qty_input_number'], value=str(quantity), timeout=5, fail_if_not_exist=False)

            self.get(self.data['cart']['add_to_cart_btn'], None, False).click()

            time.sleep(2)  

        print("FINALIZADA LA EJECUCION DE LA ORDEN <---\r\n")

    def set_checkout(self):
        self.nav(self.data['checkout']['checkout_page'])

        time.sleep(1)

        if self.data['checkout']['shipping']['ID:billing_state'] == "CABA":
            self.data['checkout']['shipping']['ID:billing_state'] = "Ciudad Autónoma de Buenos Aires"

        # Rellenar los campos de shipping
        for selector, value in self.data['checkout']['shipping'].items():
            self.fill(selector, value)

        # Rellenar los campos tipo "radio" --- no es una solucion 100 fiable o estable
        """
        Otra posibilidad es usar get_input_by_label_text() que soporta substrings pero no funciona correctamente

        Ej:
        
        self.get_input_by_label_text("Moto GRAN BUENOS AIRES").click()  # por texto en la label
        """
        for selector, value in self.data['checkout']['radios'].items():
            time.sleep(5)
            Label.click(self.driver, value)

        # Enviar pedido (presionar boton)
        if (not automation.skips['submit']):
            time.sleep(1)
            self.click_selector(self.data['checkout']['submit_btn'])

        print("Terminado el trabajo con el Checkout. ---")


    def wait_for_cart_items(self):
        """
        Espera hasta que la cantidad de elementos en el carrito sea mayor a cero.
        """
        self.wait_until_elements_present('CSS_SELECTOR:div.cart-contents')

    def wait_for_cart_items_decrease(self, previous_count):
        """
        Espera hasta que la cantidad de elementos con a.remove decrezca en una unidad.
        Args:
            previous_count (int): La cantidad anterior de elementos en el carrito.
        """
        self.wait_until_elements_decrease('CSS_SELECTOR:a.remove', previous_count)

    def wait_until_elements_present(self, selector, timeout=10):
        """
        Espera hasta que al menos un elemento identificado por el selector esté presente en la página.
        """
        self.get(selector, timeout=timeout)

    def wait_until_elements_decrease(self, selector, previous_count, timeout=10):
        """
        Espera hasta que la cantidad de elementos identificados por el selector sea menor que previous_count.
        """
        while True:
            current_count = len(self.get_all(selector, timeout=timeout))
            if current_count < previous_count:
                break
            time.sleep(0.5)

    def clear_cart(self):
        """
        Limpia el carrito (de momento con el selector "a.remove")
        """
        while True:
            # Espera hasta que la cantidad de elementos en el carrito sea mayor a cero
            self.wait_for_cart_items()

            # Encuentra todos los elementos "a.remove" en el carrito
            remove_links = self.get_all('CSS_SELECTOR:a.remove')

            # Si no hay elementos "a.remove", salir del bucle
            if not remove_links:
                break

            # Hacer clic en cada enlace "a.remove"
            for remove_link in remove_links:
                remove_link.click()

                # Esperar a que la cantidad de elementos con a.remove decrezca en una unidad
                self.wait_for_cart_items_decrease(len(remove_links))

                # Esperar un breve tiempo antes de repetir el proceso
                time.sleep(1)

    def empty_directory(self, directory):
        # Verificar si el directorio existe
        if not os.path.exists(directory):
            print(f"El directorio '{directory}' no existe.")
            return

        # Obtener la lista de archivos en el directorio
        files = os.listdir(directory)

        # Eliminar cada archivo en el directorio
        for file in files:
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Archivo '{file}' eliminado.")

        print(f"Se han eliminado todos los archivos de '{directory}'.")

    def main(self):
        try:
            if len(sys.argv) != 2:
                print("Usage: python router.py <test_file>")
                return

            loader = InstructionLoader()

            test_file         = sys.argv[1]
            instructions      = loader.load_instructions(test_file)
            self.data = instructions.get('data')
           
            login = self.data['login']
            
            self.set_base_url(login['site_url'])

            """
            Ajustes al web driver
            """

            # self.driver.implicitly_wait(10)
            self.driver.maximize_window()

            # self.cloudflareChallenge()
            # time.sleep(20)

            """
            Login
            """
            
            self.empty_directory("screenshots")
            
            if (not automation.skips['login']):
                self.login(login['slug'], login['selectors'], login['log'], login['pwd'])
                self.take_screenshot('after_login')
            
            """
            Carrito
            """

            if (not automation.skips['cart_1']):
                cart_items = self.get_cart_items()
                self.print_cart_items(cart_items)
                self.take_screenshot('after_prev_cart')


            # self.quit()

            """
            Orden
            """

            if (not automation.skips['order']):
                self.process_order()
                self.take_screenshot('after_order')

            """
            Carrito
            """

            if (not automation.skips['cart_2']):
                cart_items = self.get_cart_items()
                self.print_cart_items(cart_items)
                self.take_screenshot('cart_after_order')

            """
            Checkout
            """

            if (not automation.skips['checkout']):
                self.set_checkout()
                self.take_screenshot('after_checkout')

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

    # Skip en True implica NO ejecutar
    automation.skips = {
        "login"   : False,
        "cart_1"  : False,
        "order"   : False,
        "cart_2"  : False,
        "checkout": False,
        "submit"  : True,
    }

    # 
    # .env
    #
    # pip install python-dotenv
    #
    # https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1
    #

    load_dotenv()

    automation.is_prod  = (os.getenv('IS_PRODUCTION') == 'True')
    automation.headless = automation.is_prod or (os.getenv('OPT_HEADLESS') == 'True')

    web_driver = os.getenv('WEB_DRIVER')

    automation.setup(automation.headless, False, web_driver)
    automation.main()
