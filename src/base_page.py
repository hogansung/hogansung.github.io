from abc import abstractmethod


class BasePage(object):
    _dict = {
            'BACKGROUND_CLASS': 'normal-full',
            'PADDING': '100',
            'INDEX_URL': 'index.html',
            'HOME_URL': 'home.html',
            'BLOG_URL': 'blog.html',
            'PROJECT_UNDERGRAD_URL': 'project_undergrad.html',
            'PROJECT_GRADUATE_URL': 'project_graduate.html',
            'RESEARCH_URL': 'research.html',
            'ABOUT_URL': 'about.html',
            'HOME_LINK': 'nav-link',
            'BLOG_LINK': 'nav-link',
            'PROJECT_UNDERGRAD_LINK': 'dropdown-item',
            'PROJECT_GRADUATE_LINK': 'dropdown-item',
            'RESEARCH_LINK': 'nav-link',
            'ABOUT_LINK': 'nav-link',
    }
    _extra_dict = {}

    @property
    @abstractmethod
    def _base_name(self):
        pass

    @classmethod
    def _update_dict(cls):
        cls._dc_dict = cls._dict.copy()
        cls._dc_dict.update({
            cls._base_name+'_URL': '#',
        })
        if cls._base_name+'_LINK' in cls._dict.keys():
            cls._dc_dict.update({
                cls._base_name+'_LINK': cls._dict[cls._base_name+'_LINK'] + ' active',
            })
        cls._dc_dict.update(cls._extra_dict)

    @classmethod
    def fetch_prefix_template(cls):
        with open('template/prefix.txt') as f:
            lines = f.readlines()
        return ''.join(lines)

    @classmethod
    def fetch_suffix_template(cls):
        with open('template/suffix.txt') as f:
            lines = f.readlines()
        return ''.join(lines)

    @classmethod
    def customize_prefix(cls):
        prefix_template = cls.fetch_prefix_template()
        return prefix_template.format(**cls._dc_dict)

    @classmethod
    def customize_content(cls):
        raise(NotImplementedError)

    @classmethod
    def customize_suffix(cls):
        suffix_template = cls.fetch_suffix_template()
        return suffix_template

    @classmethod
    def render(cls):
        page_str = ''
        page_str += cls.customize_prefix()
        page_str += cls.customize_content()
        page_str += cls.customize_suffix()
        return page_str

    @classmethod
    def run(cls):
        cls._update_dict()
        file_name = cls._base_name.lower() + '.html'
        with open(file_name, 'w') as f:
            f.write(cls.render())

    @classmethod
    def clean(cls):
        raise(NotImplementedError)
