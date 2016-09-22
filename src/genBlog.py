import os
import time
import re
import hashlib


target_file = '../blog.html'
target_folder = '../blog/'
PREVIEW_LIMIT = 200

# s/!\[\](\(.*\))/<img\ src="\1"\ alt="Image Missing"\ style="width:\ 200px;"\/>/g


def cleanArticle():
    fileNames = os.listdir('../article-pages/')
    articleNames = filter(lambda x: x.find('article') >= 0, fileNames)

    for articleName in articleNames:
        os.remove(os.path.join('../article-pages/', articleName))


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
                        <li class="active"><a href="blog.html">BLOG</a></li>
                        <li><a href="research.html">RESEARCH</a></li>
                        <li><a href="about.html">ABOUT</a></li>
                    </ul>
                </div><!-- /.navbar-collapse -->
            </div><!-- /.container-fluid -->
        </nav>
        <div class="container">
'''
    return s



def getPrefix_article():
    s = '''<!DOCTYPE html>

<html lang="en" class="normal-full">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <!-- Bootstrap core CSS -->
        <link href="../bootstrap/css/bootstrap.css" rel="stylesheet">

        <!-- Bootstrap social CSS -->
        <link href="../bootstrap-social/bootstrap-social.css" rel="stylesheet">
        <link href="../bootstrap-social/assets/css/font-awesome.css" rel="stylesheet">
    </head>

    <body style="background-color: rgba(240, 250, 240, 0.3)">
        <!-- Fixed navbar -->
        <nav class="navbar navbar-default navbar-fixed-top">
            <div class="container">
                <div class="navbar-header">
                    <a class="navbar-brand" href="../index.html">Hao-en Sung (Hogan)</a>
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
                        <li><a href="../home.html">HOME</a></li>
                        <li class="active"><a href="../blog.html">BLOG</a></li>
                        <li><a href="../research.html">RESEARCH</a></li>
                        <li><a href="../about.html">ABOUT</a></li>
                    </ul>
                </div><!-- /.navbar-collapse -->
            </div><!-- /.container-fluid -->
        </nav>
        <div class="container">
'''
    return s



def getSuffix():
    s = '''        </div>

        <!-- Bootstrap core JavaScript
            ================================================== -->
            <!-- Placed at the end of the document so the pages load faster -->
            <script src="jquery/jquery-1.11.3.min.js"></script>
            <script src="bootstrap/js/bootstrap.js"></script>
    </body>
</html>'''
    return s


def getSuffix_article():
    s = '''        </div>

        <!-- Bootstrap core JavaScript
            ================================================== -->
            <!-- Placed at the end of the document so the pages load faster -->
            <script src="../jquery/jquery-1.11.3.min.js"></script>
            <script src="../bootstrap/js/bootstrap.js"></script>
    </body>
</html>'''
    return s


def extract(line):
    return re.match(r'<[^<^>]*>(.*)<[^<^>]*>', line).group(1)


def getContent(prefix, suffix):
    s = '''            <div class="page-header">
                <h1> Blog </h1>
            </div>
'''

    folderNames = os.listdir(target_folder)

    for folderName in folderNames:
        projName = os.path.join(target_folder, folderName)

        articlePath = os.path.join(projName, 'article.md')
        assert(os.path.isfile(articlePath))

        htmlPath = os.path.join(projName, 'article.html')

        # create article html
        os.system('pandoc -f markdown -t html ' + articlePath + ' -o ' + htmlPath) 

        # get information from html
        lines = open(htmlPath).readlines()
        t = extract(lines[0])
        st = extract(lines[1])
        gs = extract(lines[2])
        content = ''.join([' ' * 20 + line for line in lines[3:]])
        
        # create article hash
        articleHash = hashlib.md5(open(articlePath, 'rb').read()).hexdigest()
        target_site = os.path.join('../article-pages/', 'article_'+ articleHash + '.html')

        # for blog content
        s += '''
            <div class="row">
                <div class="col-md-12">
                    <h3> ''' + t + ''' </h3>
                    <h4> ''' + st + ''' </h4>
                    <p> ''' + gs[:PREVIEW_LIMIT]
                    
        if len(gs) > PREVIEW_LIMIT:
            s += '...'

        # hack: delete "../" for href
        s += '''
                        <a href="''' + target_site[3:] + '''"> (Read More) </a>
                    </p>
                </div>
            </div>

            <!-- /.row -->
            <hr>
'''

        # for article content
        mtime = time.ctime(os.path.getmtime(articlePath))
        ss = '''
            <div class="row">
                <div class="col-md-12">
                    <h2> ''' + t + ''' </h2>
                    <h3> ''' + st + ''' </h3>

                    <!-- /.row -->
                    <hr>

                    <p> <span class="glyphicon glyphicon-pencil"></span> ''' + ' Last edited on ' + mtime + ''' </p>

                    <!-- /.row -->
                    <hr>

                    <!-- Below content is auto-generated by pandoc -->

''' + content + '''
                    <!-- Above content is auto-generated by pandic -->

                    <!-- /.row -->
                    <hr>

                </div>
            </div>
'''

        with open(target_site, 'w') as f:
            f.write(prefix + ss + suffix)
            
    return s


def main():
    cleanArticle()

    prefix_article = getPrefix_article()
    suffix_article = getSuffix_article()
    content = getContent(prefix_article, suffix_article)

    prefix = getPrefix()
    suffix = getSuffix()
    with open(target_file, 'w') as f:
        f.write(prefix + content + suffix)


if __name__ == '__main__':
    main()
