from abc import ABCMeta, abstractproperty


class BasePage(object, metaclass=ABCMeta):
    def __init__(self):
        self._dict = {
                'BACKGROUND_CLASS': 'normal-full',
                'FACEBOOK_MODERATION': '',
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
                'PATH_PREFIX': '',
        }
        self._extra_dict = {}

    @abstractproperty
    def _base_name(self):
        pass

    def _update_dict(self):
        self._dc_dict = self._dict.copy()
        if self._base_name+'_URL' in self._dict.keys():
            self._dc_dict.update({
                self._base_name+'_URL': '#',
            })
        if self._base_name+'_LINK' in self._dict.keys():
            self._dc_dict.update({
                self._base_name+'_LINK': self._dict[self._base_name+'_LINK'] + ' active',
            })
        self._dc_dict.update(self._extra_dict)

    def fetch_prefix_template(self):
        with open('template/prefix.txt') as f:
            lines = f.readlines()
        return ''.join(lines)

    def fetch_suffix_template(self):
        with open('template/suffix.txt') as f:
            lines = f.readlines()
        return ''.join(lines)

    def customize_prefix(self):
        prefix_template = self.fetch_prefix_template()
        return prefix_template.format(**self._dc_dict)

    def customize_content(self):
        raise(NotImplementedError)

    def customize_suffix(self):
        suffix_template = self.fetch_suffix_template()
        return suffix_template.format(**self._dc_dict)

    def render(self):
        page_str = ''
        page_str += self.customize_prefix()
        page_str += self.customize_content()
        page_str += self.customize_suffix()
        return page_str

    def run(self):
        self._update_dict()
        file_name = self._base_name.lower() + '.html'
        with open(file_name, 'w') as f:
            f.write(self.render())

    def clean(self):
        raise(NotImplementedError)
