login_data = {
    "site_url": "https://www.silnari.com/",
    "log": "pablo", # crear la cuenta
    "pwd": "NsoslQPiaHQ0", # crear la cuenta
    "login_page": "?page_id=5902",
    "selectors": {
        "username_input":    'input[name="login_email"]',
        "password_input":    'input[name="login_password"]',
        "remember_checkbox": 'input[name="login_remember"]',
        "submit_button":     'ID:login-btn'
    }
}

cart_page        = "?page_id=978"
checkout_page    = "?page_id=979"

qty_input_number = "CSS_SELECTOR:input[type='number'][name='quantity']"
add_to_cart_btn  = "NAME:add-to-cart"

order_to_exe = {
    "products": [
        {
            "slug": "/cheesecakes/torta-nina",
            "qty": 1,
            "attrs": {
                "NAME:selecttalla": "U",
                "NAME:selectcolor": "crema"
            }
        },
    ],

   "client": {
        "shipping_addr": {
            "billing_first_name": "Pepito",
            "billing_last_name": "Perez",
            "billing_address_1": "Calle Principal 777",
            "billing_address_2": "Piso 5, Depto. B",
            "billing_city": "Ciudad Principal",
            "billing_postcode": "12345",
            "billing_state": "Arizona"
        },
        "customer": {
            "phone": "1234567890"
        }
    },

    "order_comments": "Por favor, entregar antes del martes."
}

