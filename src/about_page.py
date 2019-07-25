from base_page import BasePage

class AboutPage(BasePage):
    _file_name = 'about.html'
    _url_name = 'ABOUT_URL'

    @classmethod
    def customize_content(cls):
        return '''        <div class="container">
            <div class="page-header">
                <h2> About </h2>
            </div>

            <hr>

            <div class="row">
                <div class="col-md-12">
                    <h4> Education </h4>
                    <ul>
                        <li>
                            <h5><strong> University of California, San Diego </strong></h5>
                            <div style="float: right">
                                <h6><em> Sep. 2016 - Dec. 2017 </em></h6>
                            </div>
                            <ul>
                                <li><h6> M.S. in Computer Science and Engineering (CSE) </h6></li>
                                <li><h6> GPA: 3.96/4.00 (Operating System: 3.70; Randomized Algorithm: 3.70) </h6></li>
                                <li><h6> Selected courses: Latent Variable Model, Deep Learning, Computer Vision, Robotics </h6></li>
                            </ul>
                        </li>
                        <li>
                            <h5><strong> National Taiwan University </strong></h5>
                            <div style="float: right">
                                <h6><em> Sep. 2011 - June 2015 </em></h6>
                            </div>
                            <ul>
                                <li><h6> B.S. in Computer Science and Information Engineering (CSIE) </h6></li>
                                <li><h6> Major GPA: 4.04/4.30 </h6></li>
                                <li><h6> Total GPA: 3.94/4.30 </h6></li>
                                <li><h6> Selected courses: Software Engineering, Object-oriented Programming, Social Network </h6></li>
                            </ul>
                        </li>
                    </ul>

                    <h4> Work Experience </h4>
                    <ul>
                        <li>
                            <h5><strong> Full-time Machine Learning Engineer in Ads Platform, </strong> <i> Yelp </i>, </strong> <i> San Francisco </i></h5>
                            <div style="float: right">
                                <h6><em> Mar 2018 - Current </em></h6>
                            </div>
                            <ul>
                                <li><h6> Iterated on training pipeline: built features with feedback loops and make generalized model </h6></li>
                                <li><h6> Productionized the very first objective model in Yelp and increased lead counts by 111.77% <br> and lower cost-per-lead by 20.98%  </h6></li>
                                <li><h6> Customized service areas for different businesses and advertisers </h6></li>
                                <li><h6> Mentored two industry engineers </h6></li>

                                <li><h6> Team managers: Xun, Sundeep </h6></li>
                            </ul>
                        </li>
                        <li>
                            <h5><strong> Part-time Machine Learning Engineer in Ads Targeting, </strong> <i> Yelp </i>, </strong> <i> San Francisco </i></h5>
                            <div style="float: right">
                                <h6><em> Oct 2017 - Dec 2017 </em></h6>
                            </div>
                            <ul>
                                <li><h6> Built an internal tool using Spark to fetch needed information for analyses on bad advertisements </h6></li>
                                <li><h6> Mentor: Eyenaz Alaei</h6></li>
                                <li><h6> Team manager: Anusha </h6></li>
                            </ul>
                        </li>
                        <li>
                            <h5><strong> Intern Machine Learning Engineer in Ads Targeting, </strong> <i> Yelp </i>, </strong> <i> San Francisco </i></h5>
                            <div style="float: right">
                                <h6><em> Jun 2017 - Sep 2017 </em></h6>
                            </div>
                            <ul>
                                <li><h6> Improve model training pipeline; add features into Logistic Regression model and reduce cross-entropy </h6></li>
                                <li><h6> Add features into Logistic Regression model and reduce cross-entropy </h6></li>
                                <li><h6> Mentor: Niloy Gupta </h6></li>
                                <li><h6> Team manager: Anusha </h6></li>
                            </ul>
                        </li>
                        <li>
                            <h5><strong> Full-time Research Assistant, </strong> <i> Academia Sinica </i></h5>
                            <div style="float: right">
                                <h6><em> Nov 2015 - Jun 2016 </em></h6>
                            </div>
                            <ul>
                                <li><h6> Finished one paper and later submitted it to PAKDD as first author (refer to: <strong>Publications</strong>) </h6></li>
                                <li><h6> Advisor: Prof. Mi-yen Yeh </h6></li>
                            </ul>
                        </li>
                        <li>
                            <h5><strong> Full-time Research Assistant, </strong> <i> Intel-NTU Connected Context Computing Center </i></h5>
                            <div style="float: right">
                                <h6><em> May 2015 - Nov 2015 </em></h6>
                            </div>
                            <ul>
                                <li><h6> Topic: Intel Smart Car and Driving Behavior Analysis </h6></li>
                                <li><h6> Analyzed driving behavior with models written in Python and achieve 0.84 AUC performance </h6></li>
                                <li><h6> Presented results with GUI implemented in Python in 2015 Intel Asia Innovation Summit </h6></li>
                                <li><h6> Advisor: Prof. Yi-ping Hung </h6></li>
                            </ul>
                        </li>
                        <li>
                            <h5><strong> Undergraduate Research Assistant, </strong> <i> Machine Discovery and Social Network Mining Lab </i></h5>
                            <div style="float: right">
                                <h6><em> Jul 2013 - Present </em></h6>
                            </div>
                            <ul>
                                <li><h6> Topic: Recommendation of Serial Locations given Check-in Data and Friendship </h6></li>
                                <li><h6> Solved one-day route recommendation with improved Bayesian model programmed in Python </li></h6>
                                <li><h6> Advisor: Prof. Shou-de Lin </h6></li>
                            </ul>
                        </li>
                    </ul>

                    <h4> Publications </h4>
                    <ul>
                        <li>
                            <h5><strong> A Classification Model for Diverse and Noisy Labelers, </strong> <i> accepted regular paper in PAKDD'17 </i></h5>
                            <div style="float: right">
                                <h6><em> Apr 2017 </em></h6>
                            </div>
                            <ul>
                                <li><h6> First author paper, cooperated with Kuan Chen </li></h6>
                                <li><h6> Derived Graph-based model in C++ and Python to handle annotations from labelers to items </h6></li>
                                <li><h6> Advisor: Prof. Mi-yen Yeh and Prof. Shou-de Lin </h6></li>
                            </ul>
                        </li>
                        <li>
                            <h5><strong> Two-dimensional Proximal Constraints with Group Lasso for Disease Progression Prediction </strong>,<br><i> pending regular journal in IEEE TKDE</i></h5>
                            <div style="float: right">
                                <h6><em> May 2017 </em></h6>
                            </div>
                            <ul>
                                <li><h6> First author paper, individual work </li></h6>
                                <li><h6> Extended multitask learning algorithms from 1D constraints to 2D ones with Matlab and C++ </h6></li>
                                <li><h6> Advisor: Prof. Mi-yen Yeh and Prof. Shou-de Lin </h6></li>
                            </ul>
                        </li>
                    </ul>

                    <h4> Other Research Experience </h4>
                    <ul>
                        <li>
                            <h5><strong> College Student Research Project, </strong> <i> National Science Council </i></h5>
                            <div style="float: right">
                                <h6><em> Feb 2014 - Feb 2015 </em></h6>
                            </div>
                            <ul>
                                <li><h6> Topic: Real-time Classification with Missing Data given Model </h6></li>
                                <li><h6> Proposed iterative imputing framework in R for data with great amount of missing values </li></h6>
                                <li><h6> Advisor: Prof. Shou-de Lin </h6></li>
                            </ul>
                        </li>
                        <li>
                            <h5><strong> Knowledge Discovery and Data Mining Cup </strong></h5>
                            <div style="float: right">
                                <h6><em> Apr 2014 - Aug 2014 </em></h6>
                            </div>
                            <ul>
                                <li><h6> Topic: Predicting Excitement at DonorsChoose.org </h6></li>
                                <li><h6> Collaborated with three labs 15 hours a week with models programmed in Python and MySQL </li></h6>
                                <li><h6> Ranked 8th out of 472 teams in the most famous machine learning competition </li></h6>
                                <li><h6> Advisor: Prof. Shou-de Lin and Prof. Chih-Jen Lin </h6></li>
                            </ul>
                        </li>
                    </ul>

                    <h4> Awards and Honors </h4>
                    <ul>
                        <li><h6>
                            <h5><strong> Big Data Analytics for Semiconductor Manufacturing, </strong> <i> TSMC </i></h5>
                            <div style="float: right">
                                <h6><em> Year 2015 </em></h6>
                            </div>
                            <ul>
                                <li><h6> Awards for Excellent Performance out of 124 teams </h6></li>
                                <li><h6> Directed a team of three members with R programming language </li></h6>
                                <li><h6> Advisor: Prof. Hsuan-tien Lin </h6></li>
                            </ul>
                        </h6></li>
                        <li><h6>
                            <h5><strong> ACM ICPC Regional Programming Contest </strong></h5>
                            <div style="float: right">
                                <h6><em> Year 2013 </em></h6>
                            </div>
                            <ul>
                                <li><h6> Awards for ranked 4th place out of 67 teams </h6></li>
                                <li><h6> Solved 8 of 11 challenging coding problems with C++ </h6></li>
                                <li><h6> Advisor: Prof. Pu-Jen Cheng </h6></li>
                            </ul>
                        </h6></li>
                    </ul>

                    <h4> Skills </h4>
                    <ul>
                        <li>
                            <h5><strong> Programming Skills </strong></h5>
                            <ul>
                                <li><h6> Programming languages:
                                    <div class="row">
                                        <div class="col-md-10">
                                            <h6> C (C++) </h6>
                                            <div class="progress">
                                                <div class="progress-bar" role="progressbar" aria-valuenow="95" aria-valuemin="0" aria-valuemax="100" style="width: 95%">
                                                    95% <span class="sr-only"></span>
                                                </div>
                                            </div>

                                            <h6> Python </h6>
                                            <div class="progress">
                                                <div class="progress-bar" role="progressbar" aria-valuenow="90" aria-valuemin="0" aria-valuemax="100" style="width: 90%">
                                                    90% <span class="sr-only"></span>
                                                </div>
                                            </div>

                                            <h6> Java </h6>
                                            <div class="progress">
                                                <div class="progress-bar" role="progressbar" aria-valuenow="80" aria-valuemin="0" aria-valuemax="100" style="width: 80%">
                                                    80% <span class="sr-only"></span>
                                                </div>
                                            </div>

                                            <h6> Matlab </h6>
                                            <div class="progress">
                                                <div class="progress-bar" role="progressbar" aria-valuenow="65" aria-valuemin="0" aria-valuemax="100" style="width: 65%">
                                                    65% <span class="sr-only"></span>
                                                </div>
                                            </div>

                                            <h6> R </h6>
                                            <div class="progress">
                                                <div class="progress-bar" role="progressbar" aria-valuenow="65" aria-valuemin="0" aria-valuemax="100" style="width: 65%">
                                                    65% <span class="sr-only"></span>
                                                </div>
                                            </div>

                                            <h6> Ocaml </h6>
                                            <div class="progress">
                                                <div class="progress-bar" role="progressbar" aria-valuenow="35" aria-valuemin="0" aria-valuemax="100" style="width: 35%">
                                                    35% <span class="sr-only"></span>
                                                </div>
                                            </div>

                                            <h6> Golang </h6>
                                            <div class="progress">
                                                <div class="progress-bar" role="progressbar" aria-valuenow="35" aria-valuemin="0" aria-valuemax="100" style="width: 35%">
                                                    35% <span class="sr-only"></span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </h6></li>

                                <li><h6> Uitlity languages:
                                     <div class="row">
                                        <div class="col-md-10">
                                            <h6> Latex </h6>
                                            <div class="progress">
                                                <div class="progress-bar" role="progressbar" aria-valuenow="95" aria-valuemin="0" aria-valuemax="100" style="width: 95%">
                                                    95% <span class="sr-only"></span>
                                                </div>
                                            </div>

                                            <h6> Markdown </h6>
                                            <div class="progress">
                                                <div class="progress-bar" role="progressbar" aria-valuenow="80" aria-valuemin="0" aria-valuemax="100" style="width: 80%">
                                                    80% <span class="sr-only"></span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </h6></li>
                                <li><h6> Machine learning tools:
                                    <div class="row">
                                        <div class="col-md-10">
                                            <h6> Scikit-learn </h6>
                                            <div class="progress">
                                                <div class="progress-bar" role="progressbar" aria-valuenow="95" aria-valuemin="0" aria-valuemax="100" style="width: 95%">
                                                    95% <span class="sr-only"></span>
                                                </div>
                                            </div>

                                            <h6> R packages </h6>
                                            <div class="progress">
                                                <div class="progress-bar" role="progressbar" aria-valuenow="70" aria-valuemin="0" aria-valuemax="100" style="width: 70%">
                                                    70% <span class="sr-only"></span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </h6></li>
                            </ul>
                        </li>

                        <li>
                            <h5><strong> Communication Skills  </strong></h5>
                            <ul>
                                <li><h6> Real-world languages: fluent English, native Chinese, limited Taiwanese </h6></li>
                                <li><h6> Leadership: almost always the leader in school projects </h6></li>
                            </ul>
                        </li>
                    </ul>
                </div>
            </div>

            <div class="row">
                <div class="col-md-12">
                    <h4> Contact </h4>
                    <a class="btn btn-social-icon btn-facebook" target="_blank" href="https://www.facebook.com/wrangle1005">
                        <i class="fa fa-facebook"></i>
                    </a>
                    <a class="btn btn-social-icon btn-github" target="_blank" href="https://github.com/hogansung/">
                        <i class="fa fa-github"></i>
                    </a>
                    <a class="btn btn-social-icon btn-google" target="_blank" href="https://plus.google.com/+%E5%AE%8B%E6%98%8A%E6%81%A9/posts">
                        <i class="fa fa-google"></i>
                    </a>
                    <a class="btn btn-social-icon btn-linkedin" target="_blank" href="https://tw.linkedin.com/in/hao-en-sung">
                        <i class="fa fa-linkedin"></i>
                    </a>

                    <a class="btn btn-link" href="mailto:wrangle1005@gmail.com" style="border: 0; padding: 0">
                        <img src="./images/email.svg" style="width: 35px">
                    </a>
                </div>
            </div>

            <hr>
        </div>'''

    @classmethod
    def render(cls):
        page_str = ''
        page_str += cls.customize_prefix()
        page_str += cls.customize_content()
        page_str += cls.customize_suffix()
        return page_str
