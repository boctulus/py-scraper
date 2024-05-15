from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Label:
    # Script para incluir jQuery si no está disponible
    INJECT_JQUERY = '''
    if (typeof jQuery == 'undefined') {
        var script = document.createElement('script');
        script.src = 'https://code.jquery.com/jquery-3.6.0.min.js';
        document.head.appendChild(script);
    }
    '''

    # Script para hacer clic en el label
    SELECT_BY_VALUE = '''
    jQuery("label[for='" + arguments[0] + "']").click();
    '''

    @staticmethod
    def click(driver, value: str):
        # Inyectar jQuery si no está disponible
        driver.execute_script(Label.INJECT_JQUERY)
        # Esperar a que jQuery esté disponible
        WebDriverWait(driver, 10).until(lambda d: d.execute_script("return typeof jQuery != 'undefined';"))
        # Ejecutar el script para hacer clic en el label

        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//label[@for='" + value + "']"))
        )
        
        driver.execute_script("arguments[0].scrollIntoView(true);", element)

        driver.execute_script(Label.SELECT_BY_VALUE, value)

