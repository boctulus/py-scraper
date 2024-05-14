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
            "slug": "?product=chaqueta-marinera",
            "qty": 1,
            "attrs": {
                "NAME:selecttalla": "U",
                "NAME:selectcolor": "crema"
            }
        },
        {
            "slug": "?product=musculosa-coral",
            "qty": 5,
            "attrs": {
                "NAME:selecttalla": "U",
                "NAME:selectcolor": "negro"
            }
        },
         {
            "slug": "?product=pantalones-vaquero",
            "qty": 1,
            "attrs": {
                "NAME:selecttalla": "U",
                "NAME:selectcolor": "blano"
            }
        },
    ],

   "checkout": {
        "shipping": {
            "XPATH://input[@id='billing_first_name']": "Adriana",
            "XPATH://input[@id='billing_last_name']": "Fulana",
            "ID:billing_address_1": "Calle Principal 321",
            "ID:billing_address_2": "Piso 1, Depto. C",
            "ID:billing_city": "Palermo viejo",
            "ID:billing_postcode": "12345",
            "ID:billing_country": "Argentina",
            "ID:billing_state": "CABA",
            "ID:billing_wc_enviamelo_dni": "12345678",
            "NAME:order_comments": "Una nota cualquiera",
            "NAME:shipping_method": "flat_rate:7"
        },
        "customer": {
            "ID:billing_phone": "1234567890"
        }       
    },

    
}

