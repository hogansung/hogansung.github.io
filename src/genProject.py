import os


target_file = '../project.html'
target_folder = '../project/'

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
        <link href="bootstrap/css/bootstrap.css" rel="stylesheet">

        <!-- Bootstrap social CSS -->
        <link href="bootstrap-social/bootstrap-social.css" rel="stylesheet">
        <link href="bootstrap-social/assets/css/font-awesome.css" rel="stylesheet">

        <!-- Manual CSS -->
        <link href="src/manual.css" rel="stylesheet">
    </head>

    <body style="background-color: rgba(240, 250, 240, 0.3)">
        <!-- Fixed navbar -->
        <nav class="navbar navbar-default navbar-fixed-top">
            <div class="container">
                <div class="navbar-header">
                    <a class="navbar-brand" href="index.html">Hao-en Sung (Hogan)</a>
                    <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse"> 
                        <span class="sr-only">Toggle navigation</span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </button>
                </div>

                <!-- Collect the nav links, forms, and other content for toggling -->
                <div class="collapse navbar-collapse">
                    <ul class="nav navbar-nav navbar-right">
                        <li><a href="home.html">HOME</a></li>
                        <li><a href="blog.html">BLOG</a></li>
                        <li class="active"><a href="project.html">PROJECT</a></li>
                        <li><a href="research.html">RESEARCH</a></li>
                        <li><a href="about.html">ABOUT</a></li>
                    </ul>
                </div><!-- /.navbar-collapse -->
            </div><!-- /.container-fluid -->
        </nav>
        <div class="container">
            <div class="page-header">
                <h3> Undergrad projects </h3>
            </div>
'''
    return s


def getSuffix():
    s = '''

        <!-- Bootstrap core JavaScript
            ================================================== -->
            <!-- Placed at the end of the document so the pages load faster -->
            <script src="jquery/jquery-1.11.3.min.js"></script>
            <script src="bootstrap/js/bootstrap.js"></script>
        </div>
    </body>
</html>'''
    return s


def getContent():
    s = ''
    folderNames = os.listdir(target_folder)
    folderNames = filter(lambda x: x[0] != '.', folderNames)

    for folderName in folderNames:
        if folderName == 'template':
            continue

        projName = os.path.join(target_folder, folderName)
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
            imagePath = os.path.join(projName, filter(lambda x: x.find('png') >= 0, fileNames)[0])
        except:
            imagePath = default_image

        with open(readmePath) as f:
            t, st, cnt = [line.strip() for line in f.readlines()]

        # hack: delete "../" for href
        s += '''
            <div class="row">
                <div class="col-md-1 vcenter"></div>
                <div class="col-md-3 vcenter">
                    <a target="_blank" href="''' + reportPath[3:] + '''">
                        <img class="img-responsive" src="''' + imagePath[3:] + '''" alt="Image missing">
                    </a>
                </div>
                <div class="col-md-7 vcenter">
                    <h4> ''' + t + ''' </h4>
                    <h5> <i> ''' + st + ''' </i> </h5>
                    <p> ''' + cnt + ''' </p>
                    <a target="_blank" class="btn btn-primary" href="''' + reportPath[3:] + '''"> 
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
            
            <!-- /.row -->
            <hr>

'''
    return s


def main():
    prefix = getPrefix()
    suffix = getSuffix()
    content = getContent()

    with open(target_file, 'w') as f:
        f.write(prefix + content + suffix)


if __name__ == '__main__':
    main()
