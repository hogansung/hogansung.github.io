from base_page import BasePage

class IndexPage(BasePage):
    _base_name = 'INDEX'
    _extra_dict = {
            'BACKGROUND_CLASS': 'index-full',
            'PADDING': '0',
    }

    @classmethod
    def customize_content(cls):
        return ''
