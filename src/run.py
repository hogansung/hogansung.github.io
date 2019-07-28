import argparse

from about_page import AboutPage
from home_page import HomePage
from index_page import IndexPage
from project_page import ProjectGraduatePage
from project_page import ProjectUnderGradPage
from research_page import ResearchPage


def main():
    AboutPage.run()
    HomePage.run()
    IndexPage.run()
    ProjectGraduatePage.run()
    ProjectUnderGradPage.run()
    ResearchPage.run()


if __name__ == '__main__':
    main()
