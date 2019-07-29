import os
import pathlib

from base_page import BasePage


class ResearchPage(BasePage):
    def __init__(self):
        super().__init__()
        self._folder = 'research'
        self._sub_folders = [
                {
                    'name': 'Accepted Papers',
                    'report_link_enabled': True,
                },
                {
                    'name': 'Pending Papers (details hidden)',
                    'report_link_enabled': False,
                },
                {
                    'name': 'Unsubmitted Works',
                    'report_link_enabled': True,
                },
        ]

    @property
    def _base_name(self):
        return 'RESEARCH'

    def customize_content(self):
        s = '''        <div class="container">
            <div class="page-header">
                <h2> Research </h2>
            </div>
'''

        for sub_folder_info in self._sub_folders:
            sub_folder = sub_folder_info['name']
            report_link = sub_folder_info['report_link_enabled']

            if not os.path.exists(os.path.join(self._folder, sub_folder)):
                continue

            folder_names = os.listdir(os.path.join(self._folder, sub_folder))
            folder_names = [x for x in folder_names if x[0] != '.']

            s += '''            <div class="row">
                <div class="col-md-12">
                    <h3 align="center"> ''' + sub_folder + ''' </h3>
                </div>
            </div>

            <br>
'''

            for idx, folder_name in enumerate(folder_names):
                proj_name = os.path.join(self._folder, sub_folder, folder_name)
                file_names = os.listdir(proj_name)
                file_names = [x for x in file_names if x[0] != '.']

                try:
                    report_path = os.path.join(proj_name, [x for x in file_names if x.find('report') >= 0][0])
                except:
                    report_path = default_report

                try:
                    readme_path = os.path.join(proj_name, [x for x in file_names if x.find('readme') >= 0][0])
                except:
                    readme_path = default_readme

                try:
                    image_path = os.path.join(proj_name, [x for x in file_names if x.find('jpg') >= 0][0])
                except:
                    image_path = default_image

                try:
                    video_path = os.path.join(proj_name, [x for x in file_names if x.find('video') >= 0][0])
                except:
                    video_path = None

                with open(readme_path) as f:
                    lines = [line.strip() for line in f.readlines()]
                    if len(lines) == 3:
                        t, st, cnt = lines
                        abstract = keywords = ""
                    else:
                        t, st, abstract, keywords = lines[:4]
                        link = lines[4] if len(lines) == 5 else None

                # hack: get relative location
                report_p = pathlib.Path(report_path)
                rel_report_path = str(pathlib.Path(*report_p.parts))

                image_p = pathlib.Path(image_path)
                rel_image_path = str(pathlib.Path(*image_p.parts))

                # hack: deal with media
                medias = [x for x in file_names if x.find('video') >= 0]
                if len(medias) > 0:
                    with open(os.path.join(proj_name, 'media.html'), 'w') as f:
                        f.write('''<!DOCTYPE html>
<html>
<head>
</head>
<body>
    <video style="position: absolute; top: 50%; left: 50%; transform: translateX(-50%) translateY(-50%);" width="100% height="100%" controls autoplay autoplay loop preload="auto">
      <source src=''' + medias[0] + ''' type="video/mp4">
    </video>
</body>
</html>
''')

                s += '''
            <div class="row align-items-center">
                <div class="col-md-5 ">
'''
                if report_link:
                    s += '''                    <a target="_blank" href="''' + rel_report_path + '''">
'''
                else:
                    s += '''                    <a>
'''

                s += '''                        <img class="img-fluid" src="''' + rel_image_path + '''" alt="Image missing">
                    </a>
                </div>
                <div class="col-md-7 ">
                    <h4> ''' + t + ''' </h4>
                    <h5> <i> ''' + st + ''' </i> </h5>
                    <p class="auto"> <strong>Abstract:</strong> ''' + abstract + ''' </p>
                    <p> <strong>Keywords:</strong> <i>''' + keywords + '''</i> </p>
'''

                if link:
                    s += '''                    <p> <strong>Paper:</strong> <a href="''' + link + '''" target="_blank">''' + link + '''</a> </p>
'''
                else:
                    s += '''                    <p> <strong>Paper:</strong> Not available </p>
'''

                if report_link:
                    s += '''                    <a target="_blank" class="btn btn-primary" href="''' + rel_report_path + '''">
                        Get the Report
                        <span class="glyphicon glyphicon-chevron-right">
                        </span>
                    </a>
'''

                if os.path.isfile(os.path.join(proj_name, 'source.zip')):
                    s += '''                    <a class="btn btn-primary" target="_blank" href="''' + os.path.join(proj_name[3:] , 'source.zip') + '''">
                        Get the Source
                        <span class="glyphicon glyphicon-chevron-right">
                        </span>
                    </a>
'''

                if os.path.isfile(os.path.join(proj_name, 'media.html')):
                    s += '''                    <a class="btn btn-primary" target="_blank" href="''' + os.path.join(proj_name[3:] , 'media.html') + '''">
                        Get the Video
                        <span class="glyphicon glyphicon-chevron-right">
                        </span>
                    </a>
'''

                s += '''                </div>
            </div>

            <br>
'''

                if idx < len(folder_names) - 1:
                    s += '''
            <br>
            <br>
            <br>
'''

            s += '''
            <hr>
'''

        s += '''
        </div>
'''
        return s
