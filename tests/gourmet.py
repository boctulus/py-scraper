login_data = {
    'site_url': 'https://torrepadregourmet.es',
    'log': 'pablo@tiendaonline.com.ar',
    'pwd': 'pablo123$=Nn',
    'login_page': 'wp-login.php',
    'cart_page': '/cart/'
}

cart_page = '/cart/'

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
            'billing_address_1': 'Calle Principal 123',
            'billing_address_2': 'Piso 2, Depto. A',
            'billing_city': 'Ciudad Principal',
            'billing_postcode': '12345',
            'billing_state': 'Madrid'
        },
        'customer': {
            'phone': '1234567890'
        }
    },
    
    'order_comments': 'Por favor, entregar antes del sábado.'
}