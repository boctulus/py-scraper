from selenium import webdriver
from selenium.webdriver.common.by import By
from collections import namedtuple

class Select2:
    """
    Forma de uso:

    # Seleccionar el estado de facturación
    billing_state_input = self.get('ID:billing_state')

    # Obtener el elemento como un Select2 si es un Select2
    select2_countries = Select2(self.driver, billing_state_input)

    if select2_countries:
        select2_countries.selectByVisibleText('Salta') # selecciono
    else:
        print("The select element is not a Select2.")

    """

    Option = namedtuple('Option', 'text')

    # Javascript scripts -----------------------------------------------------------------------------------------------
    SELECT_BY_VALUE = \
    '''
    jQuery(arguments[0]).val(arguments[1]);
    jQuery(arguments[0]).trigger('change');
    '''

    GET_OPTIONS = \
    '''
    var myOpts = jQuery(arguments[0]).find('option');
    return myOpts;
    '''

    GET_SELECTIONS = \
    '''
    return jQuery(arguments[0]).select2('data');
    '''
    # End Javascript scripts -------------------------------------------------------------------------------------------

    def __init__(self, webdriver, element):
        self.webdriver = webdriver
        self.element   = element
        self.options   = None

    def get_options(self):
        if not self.options:
            options_elements = self.webdriver.execute_script(self.GET_OPTIONS, self.element)
            self.options = {opt.text: opt.get_attribute('value') for opt in options_elements}
        return self.options

    def selectByVisibleText(self, text):
        options = self.get_options()
        value   = options[text]
        self.webdriver.execute_script(self.SELECT_BY_VALUE, self.element, value)

    @property
    def firstSelectedOption(self):
        selections = self.webdriver.execute_script(self.GET_SELECTIONS, self.element)
        option = self.Option(selections[0]['text'])
        return option

    @staticmethod
    def isSelect2(element):
        if element:
            classes = element.get_attribute('class').split(' ')
            for class_name in classes:
                if class_name == 'select2-hidden-accessible':
                    return True
        return False
