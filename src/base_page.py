class BasePage:
    _file_name = 'base.html'
    _url_name = 'BASE_URL'
    _url_dict = {
            'HOME_URL': 'home.html',
            'BLOG_URL': 'blog.html',
            'PROJ_URL': 'project.html',
            'PROJ_UGRAD_URL': 'project_undergrad.html',
            'PROJ_GRAD_URL': 'project_graduate.html',
            'RSRCH_URL': 'research.html',
            'ABOUT_URL': 'about.html',
    }

    @classmethod
    def _update_url_dict(cls):
        cls._url_dict.update({cls._url_name: '#'})

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
        return prefix_template.format(**cls._url_dict)

    @classmethod
    def customize_suffix(cls):
        suffix_template = cls.fetch_suffix_template()
        return suffix_template

    @classmethod
    def customize_content(cls):
        raise(NotImplementedError)

    @classmethod
    def render(cls):
        raise(NotImplementedError)

    @classmethod
    def run(cls):
        cls._update_url_dict()
        with open(cls._file_name, 'w') as f:
            f.write(cls.render())

    @classmethod
    def clean(cls):
        raise(NotImplementedError)
