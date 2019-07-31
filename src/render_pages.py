import argparse

from about_page import AboutPage
from blog_page import BlogPage
from home_page import HomePage
from index_page import IndexPage
from project_page import ProjectGraduatePage
from project_page import ProjectUnderGradPage
from research_page import ResearchPage


def exec(args):
    about_page = AboutPage()
    blog_page = BlogPage()
    home_page = HomePage()
    index_page = IndexPage()
    project_graduate_page = ProjectGraduatePage()
    project_undergrad_page = ProjectUnderGradPage()
    research_page = ResearchPage()

    if args.clean:
        blog_page.clean()
        print('Clean up article pages')

    if args.thumbnail:
        project_graduate_page.generate_thumbnail()
        project_undergrad_page.generate_thumbnail()
        research_page.generate_thumbnail()
        print('Regenerate thumbnails for project and research pages')

    if args.about or args.all:
        about_page.run()
        print('About page is generated')

    if args.blog or args.all:
        blog_page.run()
        print('Blog pages are generated')

    if args.home or args.all:
        home_page.run()
        print('Home page is generated')

    if args.index or args.all:
        index_page.run()
        print('Index page is generated')

    if args.project or args.all:
        project_graduate_page.run()
        print('Graduate project page is generated')
        project_undergrad_page.run()
        print('UnderGrad project page is generated')

    if args.research or args.all:
        research_page.run()
        print('Research page are generated')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', help='render all pages at once', action='store_true')
    parser.add_argument('--clean', help='clean cached files', action='store_true')
    parser.add_argument('--about', help='render about page', action='store_true')
    parser.add_argument('--blog', help='render blog pages', action='store_true')
    parser.add_argument('--home', help='render home pages', action='store_true')
    parser.add_argument('--index', help='render index pages', action='store_true')
    parser.add_argument('--project', help='render project pages', action='store_true')
    parser.add_argument('--research', help='render research page', action='store_true')
    parser.add_argument('--thumbnail', help='generate thumbnail', action='store_true')
    args = parser.parse_args()
    exec(args)


if __name__ == '__main__':
    main()
