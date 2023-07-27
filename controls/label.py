from .base_control import BaseControl


class Label(BaseControl):
    def __init__(self, label_element):
        super().__init__(label_element)

    def get_text(self):
        return self.element.text
