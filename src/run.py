import argparse

from about_page import AboutPage
from blog_page import BlogPage
from home_page import HomePage
from index_page import IndexPage
from project_page import ProjectGraduatePage
from project_page import ProjectUnderGradPage
from research_page import ResearchPage


def main():
    about_page = AboutPage()
    blog_page = BlogPage()
    home_page = HomePage()
    index_page = IndexPage()
    project_graduate_page = ProjectGraduatePage()
    project_undergrad_page = ProjectUnderGradPage()
    research_page = ResearchPage()

    about_page.run()
    blog_page.run()
    home_page.run()
    index_page.run()
    project_graduate_page.run()
    project_undergrad_page.run()
    research_page.run()


if __name__ == '__main__':
    main()
