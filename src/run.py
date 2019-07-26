import argparse

from about_page import AboutPage
from home_page import HomePage
from index_page import IndexPage


def main():
    AboutPage.run()
    HomePage.run()
    IndexPage.run()


if __name__ == '__main__':
    main()
