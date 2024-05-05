login_data = {
    'site_url': 'https://torrepadregourmet.es',
    'log': 'pablo@tiendaonline.com.ar',
    'pwd': 'pablo123$=Nn',
    'login_page': 'wp-login.php',
    # 'selectors': {
    #     'username_input':    '[id="user_login"]',
    #     'password_input':    '[id="user_pass"]',
    #     'remember_checkbox': '[name="rememberme"]',
    #     'submit_button':     '[id="wp-submit"]'
    # }
}

cart_page = '/cart/'
checkout_page = '/checkout/'

order_to_exe = {
    'products': [
        {
            'prd': '/producto/queso-oregano-530gr/',
            'qty': 2
        },
        {
            'prd': '/producto/jamon-de-tudanca/',
            'qty': 5
        },
        {
            'prd': '/producto/chorizo-de-ciervo-300g/',
            'qty': 3
        },
    ],

   'client': {
        'shipping_addr': {
            'billing_first_name': 'Ambrosio F.',
            'billing_last_name': 'Perez Diaz',
            'billing_address_1': 'Calle Principal 777',
            'billing_address_2': 'Piso 5, Depto. B',
            'billing_city': 'Ciudad Principal',
            'billing_postcode': '12345',
            'billing_state': 'Madrid'
        },
        'customer': {
            'phone': '1234567890'
        }
    },

    'order_comments': 'Por favor, entregar antes del sabado.'
}