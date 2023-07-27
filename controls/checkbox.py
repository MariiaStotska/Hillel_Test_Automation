from .base_control import BaseControl


class CheckBox(BaseControl):
    def __init__(self, checkbox_element):
        super().__init__(checkbox_element)

    def is_checked(self):
        return self.element.is_selected()

    def check(self):
        if not self.is_checked():
            self.element.click()

    def uncheck(self):
        if self.is_checked():
            self.element.click()
