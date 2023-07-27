class BaseControl:
    def __init__(self, web_element):
        self.element = web_element

    def is_displayed(self):
        return self.element.is_displayed()
