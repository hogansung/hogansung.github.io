import argparse

from about_page import AboutPage
from home_page import HomePage
from index_page import IndexPage
from proj_page import ProjGradPage
from proj_page import ProjUGradPage


def main():
    AboutPage.run()
    HomePage.run()
    IndexPage.run()
    ProjGradPage.run()
    ProjUGradPage.run()


if __name__ == '__main__':
    main()
