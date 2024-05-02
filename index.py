from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import os

class WebAutomation:
    def __init__(self):
        self.driver = None

    def setup(self):
        options = Options()
        options.add_extension("D:\ChromeExtensions\DarkReader.crx")
        # options.add_argument("--headless")
        # options.add_argument('--headless=new')
        # options.add_argument("start-maximized")
        # options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--disable-gpu')
        # options.add_argument('--no-sandbox')
        # option.binary_location = "/path/to/google-chrome"
            
        # self.driver = webdriver.Chrome(service=ChromeService(
        #     ChromeDriverManager().install()), options=options)

        self.driver = webdriver.Chrome(options=options)

        # Resto del código...

    def login(self):
        self.driver.get(self.login_data['site_url'] + '/' + self.login_data['login_page'])
        # Resto del código...

        username_input = self.driver.find_element(By.ID, 'user_login')
        username_input.send_keys(self.login_data['log'])

        password_input = self.driver.find_element(By.ID, 'user_pass')
        password_input.send_keys(self.login_data['pwd'])

        login_button = self.driver.find_element(By.ID, 'wp-submit')
        login_button.click()

    def get_cart_items(self):
        self.driver.get(self.login_data['site_url'] + self.cart_page)
        self.driver.get(self.login_data['site_url'] + self.cart_page)
        time.sleep(5)

        cart_items = []

        product_rows = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.woocommerce-cart-form__cart-item"))
        )

        for row in product_rows:
            product_name_element = row.find_element(By.CSS_SELECTOR, "td.product-name a")
            product_name = product_name_element.text
            product_url = product_name_element.get_attribute("href")

            product_price_element = row.find_element(By.CSS_SELECTOR, "td.product-price span.woocommerce-Price-amount")
            product_price = product_price_element.text

            product_quantity_element = row.find_element(By.CSS_SELECTOR, "td.product-quantity input.input-text.qty.text")
            product_quantity = product_quantity_element.get_attribute("value")

            product_subtotal_element = row.find_element(By.CSS_SELECTOR, "td.product-subtotal span.woocommerce-Price-amount")
            product_subtotal = product_subtotal_element.text

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
            self.driver.get(self.login_data['site_url'] + product_url)
            time.sleep(2)

        p = self.Product()

        title_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h1[@class='product-title product_title entry-title']"))
        )
        p.title = title_element.text


        price_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='product-main']//bdi[1]"))
        )
        p.price = price_element.text

        description_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='product-short-description']/p"))
        )
        p.description = description_element.text

        stock_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "p.stock.in-stock"))
        )
        p.stock = stock_element.text

        sku_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span.sku"))
        )
        p.sku = sku_element.text

        # Retorna un objeto Producto
        return p

    def load_instructions(self, test_file):
        instructions = {}
        test_file_path = os.path.join('tests', test_file)
       
        if not os.path.isfile(test_file_path):
            print(f"Error: File '{test_file}' not found.")
            return

        with open(test_file_path, 'r') as f:
            exec(f.read(), instructions)
            
        return instructions

    def main(self):
        if len(sys.argv) != 2:
            print("Usage: python router.py <test_file>")
            return

        test_file = sys.argv[1]
        instructions = self.load_instructions(test_file)

        self.login_data   = instructions.get('login_data')
        self.cart_page    = instructions.get('cart_page')
        self.order_to_exe = instructions.get('order_to_exe')

        try:
            #
            # Login
            #
            
            self.login()

            self.driver.maximize_window()

            #
            # Carrito
            #

            cart_items = self.get_cart_items()
            self.print_cart_items(cart_items)


            #
            # Orden
            #

            print("COMIENZO A EJECUTAR LA ORDEN: --->\r\n")
            for products in self.order_to_exe['products']:
                product_page = products['prd']
                quantity     = products['qty']

                self.driver.get(self.login_data['site_url'] + product_page)
                time.sleep(2)

                p = self.get_product(product_page)
                self.Product.print(p)

                quantity_input = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.quantity.buttons_added input[type='number'][name='quantity']"))
                )

                quantity_input.clear()
                quantity_input.send_keys(str(quantity))

                add_to_cart_button = self.driver.find_element(By.CSS_SELECTOR, "button.single_add_to_cart_button")
                add_to_cart_button.click()
                time.sleep(3)
            print("FINALIZADA LA EJECUCION DE LA ORDEN <---\r\n")

            #
            # Carrito
            #

            cart_items = self.get_cart_items()
            self.print_cart_items(cart_items)


        finally:
            time.sleep(3)
            self.driver.quit()


if __name__ == "__main__":
    automation = WebAutomation()
    automation.setup()
    automation.main()
