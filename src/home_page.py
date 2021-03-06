from base_page import BasePage


class HomePage(BasePage):
    def __init__(self):
        super().__init__()

    @property
    def _base_name(self):
        return 'HOME'

    def customize_content(self):
        return '''        <div class="container">
            <div class="page-header">
                <h2> Home </h2>
            </div>

            <hr>

            <div class="row">
                <div class="col-md-12">
                    <h3> Some words about me </h3>
                    <br>
                    <p> I have decided to build one personalized website for many years, but have no time to fulfill this idea. Two years ago, after graduation with bachelor degree, I finally started to build my website! For now, I have finished my master degree is Univeristy of California, San Diego, and is going to work full-time in Yelp, San Francisco. </p>
                    <p> This website is designed to fulfill the following purposes:
                        <li> Share my ideas through <a href="blog.html"><strong>Blog</strong></a>; while others can give me feedback through Facebook comment and like&amp;share plugins. </li>
                        <li> Preserve and present my old project works through <a href="project_undergrad.html"><strong>Undergrad Project</strong></a>, <a href="project_graduate.html"><strong>Graduate Project</strong></a>, and <a href="research.html"><strong>Research </strong></a>. </li>
                        <li> Polish my education, work experience, research experience, and skill proficiencies through <a href="about.html"><strong> About </strong></a>. </li>
                    </p>

                    <p> Since I am a newbie to website design, there must be much room for improvements. If you have any suggestion to this website, please feel free to contact me. Several available contact approaches can be found in <a href="about.html"><strong>About</strong></a>. </p>

                    <hr>

                    <h3> Some words about website </h3>
                    <br>
                    <p> This is a completely static website, which is based on bootstrap pre-built elements. There are seven main webpages, includes <ul>
                        <li> <a href="index.html"><strong>Index</strong></a> </li>
                        <li> <a href="home.html"><strong>Home</strong></a> </li>
                        <li> <a href="blog.html"><strong>Blog</strong></a> </li>
                        <li> <a href="project_undergrad.html"><strong>Undergrad Project</strong></a> and <a href="project_graduate.html"><strong>Graduate Project</strong></a> </li>
                        <li> <a href="research.html"><strong>Research </strong></a> </li>
                        <li> <a href="about.html"><strong>About</strong></a> </li>
                    </ul> </p>
                    <p> The wepages, including <a href="index.html"><strong>Index</strong></a>, <a href="home.html"><strong>Home</strong></a>, and <a href="about.html"><strong>About</strong></a>, are easy. However, I want to elaborate my works on <a href="blog.html"><strong>Blog</strong></a>, <a href="project_undergrad.html"><strong>Undergrad Project</strong></a>, <a href="project_graduate.html"><strong>Graduate Project</strong></a>, and <a href="research.html"><strong>Research</strong></a>. </p>

                    <br>

                    <h4> How to build <strong>Blog</strong> page? </h4>
                    <p> The core idea for blog is that it should at least support font-style control, and image attachment. Furthermore, there should be a main entrance for all blog articles. To achieve this requirement automatically, I decided to provide a friendly API, which is able to not only convert markdown files to htmls, but also build up internal links between blogs properly. </p>
                    <p> To be more detailed, I first retrieve all markdown files in one folder and use Pandoc to do the markdown-to-html conversion. Later on, I sort all documents based on their `mtime`, so that newer documents can have higher priority to be viewed. At the end, I generate an entrance html, which can direct users to any article file. </p>
                    <p> In the latest version of my blog, I successively embed Facebook plugins into aricles, so that people can like, share, and leave comments on my article once he or she logins in with Facebook account. </p>

                    <br>

                    <h4> How to build <strong>Undergrad Project</strong> and <strong>Graduate Project</strong> pages? </h4>
                    <p> The main concept for both project pages is to present all my previous student project in a relatively robust way.
                    Thus, to illustrate my work in detail, I provide a brief description about the background and motivation of that project, a thumbnail of the report in jpeg format, a report in pdf format, and compressed source code (if possible). Similar to <a href="blog.html"><strong>Blog</strong></a>, I can imagine that there are going to be lots of projects. In ohter words, rendering all html pages in an automatic way is crucial for me. </p>
                    <p> To achieve automation, I first use Wand.Image to convert the fitst page of each pdf report into jpeg image. After that, what I need to do is simply render two project pages based on the information in each project folder. Initially, I stored images in png format with original sizes; however, I soon realized that it greatly slowed down the website loading speed. It turns out that resizing and jpeg format can significantly reduce the size of thumbnails. </p>

                    <br>

                    <h4> How to build <strong>Research</strong> page? </h4>
                    <p> I use a very similar approach as what I did for projects, except the thumbnails are enlarged and abstract and keywords are provided. It is noticeable that I temporarily remove the details for pending papers for confidentiality. </p>

                    <br>

                    <h4> How long did it take for me to build this site? </h4>
                    <p> In the very beginning, I spent around 30 hours in writing Python codes and examining possible frameworks for my website. For example, I have tried SemanticUI and Json but in vain. Later on, I used most of time trying to be familiar with bootstrap framework. That is basically when I have done for Version 0. </p>
                    <p> Around one year later, I realized that `github.io` is actually a better address to hold my website in the long run, so I spent some time in migraing everything from CSIE server, which is my undergrad server, to GitHub. On top of that, I also update <a href="about.html"><strong>About</strong></a> page, including adding some more demonstrative progress bars to represent my skill proficiencies. Later, I almost always mention my personal website to my interviewers when I was finding my internship and full-time job. </p>
                    <p> After I finished my master degree in UCSD, I have a couple of spare days. Thus, I decided to add some more fancy functionailities on my website, including a block for other to leave comments about my articles and a counter of how many people have visited my website. I achieved the first functionality by embeding Facebook plugins. Though there are much easier way to add a visitor counter on my website, I still choose a more robust solution: Google Analytics. The strenghs of Google Analytics is that it provides a very detailed analysis about your website; however, it is harder for one to retrieve the information. I have spent a lot of time in reading documents about the difference of `API_KEY`, `Client ID`, `Tracking ID`, and `View ID`. After working on it for a whole week, I finally finished all functionalities I have dreamed of. </p>

                    <hr>

                    <h3> Future works </h3>
                    <br>
                    <p> When there are more blogs, I need a better way to present my articles to others and not just cram everything in one page. For exmaple, I should categorize articles with some factors, such as date (month and year), tech or non-tech, or topics. Besides that, I can even migrate all my diaries into this website. </p>
                    <p><s> I can try to upgrade my website from Bootstrap V3 to Bootstrap V4. Based on the official documentation, Bootstrap V4 seems to support more fancy components and optimize the loading speed. For more details, please refer to <a href="https://v4-alpha.getbootstrap.com/migration/">Bootstrap Migrating to V4</a>.</s></p>

                    <p> My next step will be to migrate this website from GitHub to either AWS or Azure, so that I can build up my own server + database to add comments/likes functionalities. Please be patient about it :)

                    <hr>

                    <h3> Edit history </h3>
                    <br>
                    <p> Version 0.0.0 (2015-08-01): create stable webpage version for graduate school application </p>

                    <p> Version 1.0.0 (2016-09-21): migrate from CSIE server to GitHub; redesign webpage framework  </p>
                    <p> Version 1.1.0 (2016-09-22): update about.html, including adding two pulications, modifying statements, showing percentage in skills, and renewing social links; update home.html: adding Edit History block </p>
                    <p> Version 1.2.0 (2017-06-21): update publications; update intern experience (Yelp); update school GPA </p>

                    <p> Version 2.0.0 (2018-01-04): update thumbnails for each project: use MagickWand to extract the first page of every pdf file and transfer them from pdf format into png format; update about.html </p>
                    <p> Version 2.1.0 (2018-01-05): re-design the structure of project folder; update description of projects </p>
                    <p> Version 2.2.0 (2018-01-06): re-design the structure of project folder; add Facebook comment plugin; improve the loading speed of Facebook plugin; improve loading speed of thumbnails - using jpg instead of png </p>
                    <p> Version 2.3.0 (2018-01-07): add Google Analytics; add visitor count by querying Google Report API </p>
                    <p> Version 2.4.0 (2018-01-08): optimize query to Google Report API; add older&amp;newer buttons to blog articles; update home.htnl and about.html </p>
                    <p> Version 2.5.0 (2018-01-12): add readmes for Undergrad/Sophomore and Undergrad/Junior</p>
                    <p> Version 2.6.0 (2018-01-13): add readmes for Undergrad/Senior, Graduate/Fall (2016), and Graduate/Winter (2016)</p>
                    <p> Version 2.7.0 (2018-01-16): add readmes for Graduate/Spring (2016), Graduate/Fall (2017), and Research; update home.html </p>
                    <p> Version 3.0.0 (2019-04-17): bump up Bootstrap version to 4.3.1; migrate pyfiles to Python 3; update all page stylings; update themes </p>
                </div>
            </div>

            <div id="visitor_counter"></div>

            <hr>
        </div>'''
