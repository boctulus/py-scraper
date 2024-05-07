login_data = {
    "site_url": "https://pablo.tol.ar",
    "log": "pablo",
    "pwd": "NsoslQPiaHQ0",
    "login_page": "?page_id=5902",
    "selectors": {
        "username_input":    'input[name="login_username"]',
        "password_input":    'input[name="login_password"]',
        "remember_checkbox": 'input[name="login_remember"]',
        "submit_button":     'input[name="login_submit"]'
    }
}

cart_page        = "?page_id=978"
checkout_page    = "?page_id=979"

qty_input_number = "CSS_SELECTOR:input[type='number'][name='quantity']"
add_to_cart_btn  = "NAME:add-to-cart"

order_to_exe = {
    "products": [
        {
            "prd": "?product=musculosa-coral",
            "qty": 2,
            "att": {
                "NAME:selecttalla": "U",
                "NAME:selectcolor": "negro"
            }
        },
        # {
        #     "prd": "?product=chaqueta-marinera",
        #     "qty": 1,
        #     "att": {
        #         "NAME:selecttalla": "U",
        #         "NAME:selectcolor": "crema"
        #     }
        # }
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

