import os
import pathlib


targets = {
    'Undergrad Project': {
        'target_file': '../project_undergrad.html',
        'target_folder': '../project/undergrad',
        'target_sub_folders': ['Freshman (2011)', 'Sophomore (2012)', 'Junior (2013)', 'Senior (2014)'],
    },
    'Graduate Project': {
        'target_file': '../project_graduate.html',
        'target_folder': '../project/graduate',
        'target_sub_folders': ['Fall (2016)', 'Winter (2016)', 'Spring (2017)', 'Fall (2017)'],
    },
}

default_readme = '../project/template/readme.txt'
default_image = '../project/template/catch.png'
default_report = '../project/template/report.pdf'


def getPrefix():
    s = '''<!DOCTYPE html>

<html lang="en" class="normal-full">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <!-- Bootstrap core CSS -->
        <link href="src/bootstrap/css/bootstrap.css" rel="stylesheet">

        <!-- Bootstrap social CSS -->
        <link href="src/bootstrap-social/bootstrap-social.css" rel="stylesheet">
        <link href="src/bootstrap-social/assets/css/font-awesome.css" rel="stylesheet">

        <!-- Manual CSS -->
        <link href="src/css/manual.css" rel="stylesheet">
    </head>

    <body style="padding:0; background-color: rgba(240, 250, 240, 0.3)">
        <script src="https://code.jquery.com/jquery.min.js"></script>

        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-112083134-1"></script>
        <script>
            $(window).bind("load", function() {
                $.getScript('src/js/social.js', function() {});
                $.getScript('src/js/analytics.js', function() {});
            });
        </script>

        <!-- Fixed navbar -->
        <nav class="navbar navbar-default navbar-fixed-top">
            <div class="container">
                <div class="navbar-header">
                    <a class="navbar-brand" href="index.html">Hao-en Sung (Hogan)</a>
                </div>

                <!-- Collect the nav links, forms, and other content for toggling -->
                <div class="collapse navbar-collapse">
                    <ul class="nav navbar-nav navbar-right">
                        <li><a href="home.html">HOME</a></li>
                        <li><a href="blog.html">BLOG</a></li>
                        <li class="dropdown active">
                            <a class="dropdown-toggle" data-toggle="dropdown" href="#">PROJECT<span class="caret"></span></a>
                            <ul class="dropdown-menu">
                              <li><a href="project_undergrad.html">Undergrad Project</a></li>
                              <li><a href="project_graduate.html">Graduate Project</a></li>
                            </ul>
                        </li>
                        <li><a href="research.html">RESEARCH</a></li>
                        <li><a href="about.html">ABOUT</a></li>
                    </ul>
                </div><!-- /.navbar-collapse -->
            </div><!-- /.container-fluid -->
        </nav>
'''
    return s


def getSuffix():
    s = '''

        <!-- Bootstrap core JavaScript
            ================================================== -->
            <!-- Placed at the end of the document so the pages load faster -->
            <script src="src/jquery/jquery-1.11.3.min.js"></script>
            <script src="src/bootstrap/js/bootstrap.js"></script>
        </div>
    </body>
</html>'''
    return s


def getContent(name, target_folder, target_sub_folders):
    s = '''        <div class="container">
            <div class="page-header">
                <h2> ''' + name + ''' </h2>
            </div>

            <br>
'''

    for target_sub_folder in target_sub_folders:
        if not os.path.exists(os.path.join(target_folder, target_sub_folder)):
            continue

        folderNames = os.listdir(os.path.join(target_folder, target_sub_folder))
        folderNames = filter(lambda x: x[0] != '.', folderNames)

        s += '''
            <h3 align="center"> ''' + target_sub_folder + ''' </h3>
            <br>
'''

        for folderName in folderNames:
            projName = os.path.join(target_folder, target_sub_folder, folderName)
            fileNames = os.listdir(projName)
            fileNames = filter(lambda x: x[0] != '.', fileNames)

            try:
                reportPath = os.path.join(projName, filter(lambda x: x.find('report') >= 0, fileNames)[0])
            except:
                reportPath = default_report

            try:
                readmePath = os.path.join(projName, filter(lambda x: x.find('readme') >= 0, fileNames)[0])
            except:
                readmePath = default_readme

            try:
                imagePath = os.path.join(projName, filter(lambda x: x.find('jpg') >= 0, fileNames)[0])
            except:
                imagePath = default_image

            with open(readmePath) as f:
                t, st, cnt = [line.strip() for line in f.readlines()]

            # hack: get relative location
            report_p = pathlib.Path(reportPath)
            rel_reportPath = str(pathlib.Path(*report_p.parts[1:]))

            image_p = pathlib.Path(imagePath)
            rel_imagePath = str(pathlib.Path(*image_p.parts[1:]))

            s += '''            
            <div class="row">
                <div class="col-md-1 vcenter"></div>
                <div class="col-md-3 vcenter">
                    <a target="_blank" href="''' + rel_reportPath + '''">
                        <img class="img-responsive" src="''' + rel_imagePath + '''" alt="Image missing">
                    </a>
                </div>
                <div class="col-md-7 vcenter">
                    <h4> ''' + t + ''' </h4>
                    <h5> <i> ''' + st + ''' </i> </h5>
                    <p> ''' + cnt + ''' </p>
                    <a target="_blank" class="btn btn-primary" href="''' + rel_reportPath + '''"> 
                        Get the Report
                        <span class="glyphicon glyphicon-chevron-right"> 
                        </span>
                    </a>
'''

            if os.path.isfile(os.path.join(projName, 'source.zip')):
                s += '''                    <a class="btn btn-primary" target="_blank" href="''' + os.path.join(projName[3:] , 'source.zip') + '''"> 
                        Get the Source
                        <span class="glyphicon glyphicon-chevron-right"> 
                        </span>
                    </a>
'''

            s += '''                </div>
                <div class="col-md-1 vcenter"></div>
            </div>

            <br>
            <br>
'''
        s += '''
        <hr>
        <br>
'''
    return s


def main():
    prefix = getPrefix()
    suffix = getSuffix()

    for key, value in targets.items():
        with open(value['target_file'], 'w') as f:
            content = getContent(key, value['target_folder'], value['target_sub_folders'])
            f.write(prefix + content + suffix)


if __name__ == '__main__':
    main()
