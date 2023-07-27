from .base_control import BaseControl


class ImageBox(BaseControl):
    def __init__(self, image_element):
        super().__init__(image_element)

    def get_img_source(self):
        return self.element.get_attribute("src")

    def click(self):
        self.element.click()
