# Ver 1.0

login_data = {
    "site_url": "https://torrepadregourmet.es",
    "log": "pablo@tiendaonline.com.ar",
    "pwd": "pablo123$=Nn",
    "login_page": "wp-login.php",
    "selectors": {
        "username_input":    '[id="user_login"]',
        "password_input":    '[id="user_pass"]',
        "remember_checkbox": '[name="rememberme"]',
        "submit_button":     '[id="wp-submit"]'
    }
}

cart_page        = "/cart/"
checkout_page    = "/checkout/"

qty_input_number = "CSS_SELECTOR:input[type='number'][name='quantity']"
add_to_cart_btn  = "CSS_SELECTOR:button.single_add_to_cart_button"

data = {
    "products": [
        {
            "slug": "/producto/queso-oregano-530gr/",
            "qty": 2
        },
        {
            "slug": "/producto/jamon-de-tudanca/",
            "qty": 5
        },
        {
            "slug": "/producto/chorizo-de-ciervo-300g/",
            "qty": 3
        },
    ],

   "client": {
        "shipping_addr": {
            "billing_first_name": "Ambrosio F.",
            "billing_last_name": "Perez Diaz",
            "billing_address_1": "Calle Principal 777",
            "billing_address_2": "Piso 5, Depto. B",
            "billing_city": "Ciudad Principal",
            "billing_postcode": "12345",
            "billing_state": "Madrid"
        },
        "customer": {
            "phone": "1234567890"
        }
    },

    "order_comments": "Por favor, entregar antes del domingo."
}