from base_page import BasePage

class IndexPage(BasePage):
    def __init__(self):
        super().__init__()
        self._extra_dict = {
                'BACKGROUND_CLASS': 'index-full',
                'PADDING': '0',
        }

    @property
    def _base_name(self):
        return 'INDEX'

    def customize_content(self):
        return ''
