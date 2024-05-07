login_data = {
    "site_url": "http://woo5.lan",
    "log": "boctulus",
    "pwd": "!0EJEbwu)Oa!3Fd&ev",
    "login_page": "wp-login.php",
    "selectors": {
        "username_input":    '[id="user_login"]',
        "password_input":    '[id="user_pass"]',
        "remember_checkbox": '[name="rememberme"]',
        "submit_button":     '[id="wp-submit"]'
    }
}

cart_page        = "/cart"
checkout_page    = "/checkout"

qty_input_number = "CSS_SELECTOR:input[type='number'][name='quantity']"
add_to_cart_btn  = "NAME:add-to-cart"

order_to_exe = {
    "products": [
        {
            "slug": "/product/producto-x/",
            "qty": 5
        },
        {
            "slug": "/product/nicke-one-p-variable/",
            "qty": 2,
            "attrs": {
                "NAME:attribute_talla": "6",
                "NAME:attribute_color": "verde"
            }
        }
    ],

   "client": {
        "shipping_addr": {
            "billing_first_name": "Juan",
            "billing_last_name": "Perez",
            "billing_address_1": "Calle Principal 777",
            "billing_address_2": "Piso 5, Depto. B",
            "billing_city": "Ciudad Principal",
            "billing_postcode": "12345",
            "billing_state": "CABA"
        },
        "customer": {
            "phone": "1234567890"
        }
    },

    "order_comments": "Por favor, entregar antes del martes."
}

