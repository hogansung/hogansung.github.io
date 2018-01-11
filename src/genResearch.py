import os
import pathlib


targets = {
    'Research': {
        'target_file': '../research.html',
        'target_folder': '../research',
        'target_sub_folders': [
            {
                'target_sub_folder': 'Accepted Papers',
                'report_link': True,
            },
            {
                'target_sub_folder': 'Pending Papers (details hidden)',
                'report_link': False,
            },
            {
                'target_sub_folder': 'Unsubmitted Works',
                'report_link': True,
            },
        ]
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
                        <li class="dropdown">
                            <a class="dropdown-toggle" data-toggle="dropdown" href="#">PROJECT<span class="caret"></span></a>
                            <ul class="dropdown-menu">
                              <li><a href="project_undergrad.html">Undergrad Project</a></li>
                              <li><a href="project_graduate.html">Graduate Project</a></li>
                            </ul>
                        </li>
                        <li class="active"><a href="research.html">RESEARCH</a></li>
                        <li><a href="about.html">ABOUT</a></li>
                    </ul>
                </div><!-- /.navbar-collapse -->
            </div><!-- /.container-fluid -->
        </nav>

'''
    return s


def getSuffix():
    s = '''        </div>

        <!-- Bootstrap core JavaScript -->
        <script src="https://code.jquery.com/jquery.min.js"></script>
        <script src="src/bootstrap/js/bootstrap.js"></script>

        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src='https://www.google-analytics.com/analytics.js'></script>
        <script async src="https://apis.google.com/js/api.js"></script>
        <script>
            $(window).bind("load", function() {
                $.getScript('src/js/social.js', function() {});
                $.getScript('src/js/analytics.js', function() {});
            });
        </script>
    </body>
</html>'''
    return s


def getContent(name, target_folder, target_sub_folders):
    s = '''        <div class="container">
            <div class="page-header">
                <h2> ''' + name + ''' </h2>
            </div>
'''

    for info in target_sub_folders:
        target_sub_folder = info['target_sub_folder']
        report_link = info['report_link']

        if not os.path.exists(os.path.join(target_folder, target_sub_folder)):
            continue

        folderNames = os.listdir(os.path.join(target_folder, target_sub_folder))
        folderNames = filter(lambda x: x[0] != '.', folderNames)

        s += '''            <div class="row">
                <div class="col-md-12">
                    <h3 align="center"> ''' + target_sub_folder + ''' </h3>
                </div>
            </div>

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
                lines = [line.strip() for line in f.readlines()]
                if len(lines) == 3:
                    t, st, cnt = lines
                else:
                    t, st, abstract, keywords = lines[:4]
                    link = lines[4] if len(lines) == 5 else None

            # hack: get relative location
            report_p = pathlib.Path(reportPath)
            rel_reportPath = str(pathlib.Path(*report_p.parts[1:]))

            image_p = pathlib.Path(imagePath)
            rel_imagePath = str(pathlib.Path(*image_p.parts[1:]))

            s += '''            
            <div class="row">
                <div class="col-md-5 vcenter">
'''
            if report_link:
                s += '''                    <a target="_blank" href="''' + rel_reportPath + '''">
'''
            else:
                s += '''                    <a>
'''

            s += '''                        <img class="img-responsive" src="''' + rel_imagePath + '''" alt="Image missing">
                    </a>
                </div><!--
                --><div class="col-md-7 vcenter">
                    <h4> ''' + t + ''' </h4>
                    <h5> <i> ''' + st + ''' </i> </h5>
                    <p class="auto"> <strong>Abstract:</strong> ''' + abstract + ''' </p>
                    <p> <strong>Keywords:</strong> <i>''' + keywords + '''</i> </p>
'''
            
            if link:
                s += '''                    <p> <strong>Link:</strong> <a href="''' + link + '''">''' + link + '''</a> </p>
'''
            else:
                s += '''                    <p> <strong>Link:</strong> Not available </p>
'''

            if report_link:
                s += '''                    <a target="_blank" class="btn btn-primary" href="''' + rel_reportPath + '''"> 
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
            </div>

            <br>
'''
        s += '''
            <hr>
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
