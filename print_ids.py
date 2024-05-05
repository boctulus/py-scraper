import re

def print_ids_or_values(css_selectors):
    for selector_name, selector_value in css_selectors.items():
        # Buscar ID usando expresión regular
        match = re.search(r'id="([^"]+)"', selector_value)
        if match:
            # Si se encuentra un ID, imprimirlo
            print(f"{selector_name}: {match.group(1)}")
        else:
            # Si no se encuentra un ID, imprimir el valor del selector
            print(f"{selector_name}: {selector_value}")

# Diccionario de selectores CSS
default_css_selectors = {
    'username_input':    '[id="username"]',
    'password_input':    '[id="user_pass"]',
    'remember_checkbox': '[name="rememberme"]',
    'submit_button':     '[id="wp-submit"]'
}

# Llamada a la función para imprimir IDs o valores
print_ids_or_values(default_css_selectors)
