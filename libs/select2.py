from selenium import webdriver
from collections import namedtuple

class Select2:
    Option = namedtuple('Option', 'text')

    # Javascript scripts -----------------------------------------------------------------------------------------------
    SELECT_BY_VALUE = \
    '''
    $(arguments[0]).val(arguments[1]);
    $(arguments[0]).trigger('change');
    '''

    GET_OPTIONS = \
    '''
    var myOpts = document.getElementById(arguments[0]).options;
    return myOpts;
    '''

    GET_SELECTIONS = \
    '''
    return $(arguments[0]).select2('data');
    '''
    # End Javascript scripts -------------------------------------------------------------------------------------------
    
    """Drop-in replacement for Selenium Select"""
    def __init__(self, webdriver, select_id: str):
        self.webdriver = webdriver
        self.select_id = select_id
        self.options = None

    def get_options(self):
        if not self.options:
            options_elements = self.webdriver.execute_script(self.GET_OPTIONS, self.select_id)
            self.options = {opt.text: opt.get_attribute('value') for opt in options_elements}
        return self.options

    def select_by_visible_text(self, text):
        options = self.get_options()
        value = options[text]
        self.select_by_value(value)

    def select_by_value(self, value):
        self.webdriver.execute_script(self.SELECT_BY_VALUE, '#' + self.select_id, value)

    @property
    def first_selected_option(self):
        selections = self.webdriver.execute_script(self.GET_SELECTIONS, '#' + self.select_id)
        option = self.Option(selections[0]['text'])
        return option
