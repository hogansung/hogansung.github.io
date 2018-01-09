import os
import time
import re
import hashlib


target_file = '../blog.html'
target_folder = '../blog/'
PREVIEW_LIMIT = 250

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
        <script async src="https://apis.google.com/js/api.js"></script>
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
                        <li class="active"><a href="blog.html">BLOG</a></li>
                        <li class="dropdown">
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

        <!-- Facebook moderate console -->
        <meta property="fb:app_id" content="158857908084540"/>
        <meta property="og:url" content="{}"/>
        <meta property="og:title" content="{}"/>
        <meta property="og:description" content="{}"/>
        <meta property="og:type" content="website"/>
        <meta property="og:site_name" content="Hogan's Personal Website"/>

        <!-- Bootstrap core CSS -->
        <link href="../src/bootstrap/css/bootstrap.css" rel="stylesheet">

        <!-- Bootstrap social CSS -->
        <link href="../src/bootstrap-social/bootstrap-social.css" rel="stylesheet">
        <link href="../src/bootstrap-social/assets/css/font-awesome.css" rel="stylesheet">

        <!-- Manual CSS -->
        <link href="../src/css/manual.css" rel="stylesheet">
    </head>

    <body style="padding:0; background-color: rgba(240, 250, 240, 0.3)">
        <script src="https://code.jquery.com/jquery.min.js"></script>

        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-112083134-1"></script>
        <script async src="https://apis.google.com/js/api.js"></script>
        <script>{}</script>

        <!-- Fixed navbar -->
        <nav class="navbar navbar-default navbar-fixed-top">
            <div class="container">
                <div class="navbar-header">
                    <a class="navbar-brand" href="../index.html">Hao-en Sung (Hogan)</a>
                </div>

                <!-- Collect the nav links, forms, and other content for toggling -->
                <div class="collapse navbar-collapse">
                    <ul class="nav navbar-nav navbar-right">
                        <li><a href="../home.html">HOME</a></li>
                        <li class="active"><a href="../blog.html">BLOG</a></li>
                        <li class="dropdown">
                            <a class="dropdown-toggle" data-toggle="dropdown" href="#">PROJECT<span class="caret"></span></a>
                            <ul class="dropdown-menu">
                              <li><a href="../project_undergrad.html">Undergrad Project</a></li>
                              <li><a href="../project_graduate.html">Graduate Project</a></li>
                            </ul>
                        </li>
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
        <script src="src/jquery/jquery-1.11.3.min.js"></script>
        <script src="src/bootstrap/js/bootstrap.js"></script>
    </body>
</html>'''
    return s


def getSuffix_article():
    s = '''        </div>

        <!-- Bootstrap core JavaScript
        ================================================== -->
        <!-- Placed at the end of the document so the pages load faster -->
        <script src="../src/jquery/jquery-1.11.3.min.js"></script>
        <script src="../src/bootstrap/js/bootstrap.js"></script>
    </body>
</html>'''
    return s


def extract(line):
    return re.match(r'<[^<^>]*>(.*)<[^<^>]*>', line).group(1)


def getContent(prefix, suffix):
    s = '''            <div class="page-header">
                <h2> Blog </h2>
            </div>
'''

    folderNames = os.listdir(target_folder)
    folderNames = filter(lambda x: x[0] != '.', folderNames)

    # sort documents with mtime
    articleInfo = []
    for folderName in folderNames:
        projName = os.path.join(target_folder, folderName)

        articlePath = os.path.join(projName, 'article.md')
        assert(os.path.isfile(articlePath))
        htmlPath = os.path.join(projName, 'article.html')

        # create article hash
        articleHash = hashlib.md5(open(articlePath, 'rb').read()).hexdigest()

        mtime = time.ctime(os.path.getmtime(articlePath))
        articleInfo.append([mtime, articlePath, htmlPath, articleHash])

    articleInfo = sorted(articleInfo, key=lambda x: x[0], reverse=True)

    # retrieve documents in order
    for idx, val in enumerate(articleInfo):
        mtime, articlePath, htmlPathi, articleHash = val

        # create article html
        os.system('pandoc -f markdown -t html ' + articlePath + ' -o ' + htmlPath) 

        # get information from html
        lines = open(htmlPath).readlines()
        t = extract(lines[0])
        st = extract(lines[1])

        for line in lines:
            if line[:3] == '<p>':
                gs = extract(line)
                break
        content = ''.join([' ' * 20 + line for line in lines[2:]])
        
        # name the html file
        p_target = os.path.join('../article-pages/', 'article_'+ articleInfo[idx+1][3] + '.html') if idx < len(articleInfo)-1 else None
        c_target = os.path.join('../article-pages/', 'article_'+ articleHash + '.html')
        n_target = os.path.join('../article-pages/', 'article_'+ articleInfo[idx-1][3] + '.html') if idx > 0 else None

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
                        <a href="''' + c_target[3:] + '''"> (Read More) </a>
                    </p>
                </div>
            </div>

            <hr>
'''

        # preprocess url
        c_url = "https://hogansung.github.io/article-pages/article_" + articleHash + ".html"

        # preprocess script
        script = '''
            $(window).bind("load", function() {
                $.getScript('../src/js/social.js', function() {});
                $.getScript('../src/js/analytics.js', function() {});
            });
        '''

        # for article content
        ss = '''
            <div class="row">
                <div class="page-header">
                    <h2> ''' + t + ''' </h2>
                    <h3> ''' + st + ''' </h3>
                    <br>
                    <p align="right"> <span class="glyphicon glyphicon-pencil"></span> ''' + ' Last edited on ' + mtime + ''' </p>
                </div>

                <div class="col-md-12">
                    <!-- Below content is auto-generated by pandoc -->
''' + content + '''
                    <!-- Above content is auto-generated by pandoc -->

                    <br>
                    <ul class="pager">
'''

        if p_target:
            ss += '''                        <li class="previous"><a href="''' + p_target + '''">&larr; Older</a></li>
'''
        else:
            ss += '''                        <li class="previous disabled"><a>&larr; Older</a></li>
'''

        if n_target:
            ss += '''                        <li class="next"><a href="''' + n_target + '''">Newer &rarr;</a></li>
'''
        else:
            ss += '''                        <li class="next disabled"><a>Newer &rarr;</a></li>
'''

        ss += '''
                    </ul>

                    <hr>

                    <div class="fb-like" data-href=''' + c_url + ''' data-layout="standard" data-action="like" data-size="small" data-show-faces="true" data-share="true"></div>
                    <br>
                    <br>
                    <div class="fb-comments" data-href=''' + c_url + ''' data-width="100%" data-numposts="5"></div>

                    <br>
                    <br>
                </div>
            </div>
'''

        with open(c_target, 'w') as f:
            f.write(prefix.format(c_url, t, gs[:PREVIEW_LIMIT] + '...', script) + ss + suffix)
            
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
