import os
import pathlib

from abc import abstractmethod

from base_page import BasePage


class ProjectPage(BasePage):
    default_readme = 'project/template/readme.txt'
    default_image = 'project/template/catch.png'
    default_report = 'project/template/report.pdf'

    @property
    @abstractmethod
    def _folder(self):
        pass

    @property
    @abstractmethod
    def _sub_folders(self):
        pass

    @property
    @abstractmethod
    def _title(self):
        pass

    @classmethod
    def customize_content(cls):
        s = '''        <div class="container">
            <div class="page-header">
                <h2> ''' + cls._title + ''' </h2>
            </div>

'''

        for sub_folder in cls._sub_folders:
            if not os.path.exists(os.path.join(cls._folder, sub_folder)):
                continue

            folder_names = sorted(os.listdir(os.path.join(cls._folder, sub_folder)))
            folder_names = [x for x in folder_names if x[0] != '.' and x[0] != '_']

            s += '''
            <div class="row">
                <div class="col-md-12">
                    <h3 align="center"> ''' + sub_folder + ''' </h3>
                </div>
            </div>

            <br>

'''

            for folder_name in folder_names:
                proj_name = os.path.join(cls._folder, sub_folder, folder_name)
                file_names = os.listdir(proj_name)
                file_names = [x for x in file_names if x[0] != '.']

                try:
                    report_path = os.path.join(proj_name, [x for x in file_names if x.find('report') >= 0][0])
                except:
                    # report_path = default_report
                    continue

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
                    t, st, cnt = [line.strip() for line in f.readlines()]

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
                <div class="col-md-4 ">
                    <a target="_blank" href="''' + rel_report_path + '''">
                        <img class="img-fluid" src="''' + rel_image_path + '''" alt="Image missing">
                    </a>
                </div><!--
                --><div class="col-md-8 ">
                    <h4> ''' + t + ''' </h4>
                    <h5> <i> ''' + st + ''' </i> </h5>
                    <p> ''' + cnt + ''' </p>
                    <a target="_blank" class="btn btn-primary" href="''' + rel_report_path + '''">
                        Get the Report
                        <span class="glyphicon glyphicon-chevron-right">
                        </span>
                    </a>
'''

                if os.path.isfile(os.path.join(proj_name, 'source.zip')):
                    s += '''                    <a target="_blank" class="btn btn-primary" href="''' + os.path.join(proj_name , 'source.zip') + '''">
                        Get the Source
                        <span class="glyphicon glyphicon-chevron-right">
                        </span>
                    </a>
'''

                if os.path.isfile(os.path.join(proj_name, 'media.html')):
                    s += '''                    <a target="_blank" class="btn btn-primary" href="''' + os.path.join(proj_name , 'media.html') + '''">
                        Get the Video
                        <span class="glyphicon glyphicon-chevron-right">
                        </span>
                    </a>
'''

                s += '''                </div>
            </div>

            <br>
            <br>
'''
            s += '''
            <hr>
'''
        return s


class ProjectGraduatePage(ProjectPage):
    _base_name = 'PROJECT_GRADUATE'
    _folder = 'project/graduate'
    _sub_folders = ['Fall (2016)', 'Winter (2016)', 'Spring (2016)', 'Fall (2017)']
    _title = 'Graduate Project'


class ProjectUnderGradPage(ProjectPage):
    _base_name = 'PROJECT_UNDERGRAD'
    _folder = 'project/undergrad'
    _sub_folders = ['Freshman (2011)', 'Sophomore (2012)', 'Junior (2013)', 'Senior (2014)']
    _title = 'Undergrad Project'
