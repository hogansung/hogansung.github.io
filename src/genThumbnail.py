import os
import subprocess
from wand.image import Image
from wand.color import Color


def main():
    paths = ['../project/undergrad', '../project/graduate']
    
    for path in paths:
        fds = os.listdir(path)
        fds = filter(lambda x: x[0].isupper(), fds)

        for fd in fds:
            sfds = os.listdir(os.path.join(path, fd))
            sfds = filter(lambda x: x[0].isupper(), sfds)

            for sfd in sfds:
                f = os.path.join(path, fd, sfd, 'report.pdf')
                subprocess.call(['ls', f])
                all_page = Image(filename=f)
                one_page = all_page.sequence[0]

                with Image(one_page) as pg:
                    pg.format = 'png'
                    width = long(pg.width * 0.6)
                    height = long(pg.height * 0.6)
                    pg.resize(width, height)
                    pg.background_color = Color('white')
                    pg.alpha_channel = 'remove'
                    pg.save(filename=os.path.join(path, fd, sfd, 'thumbnail.png'))


if __name__ == '__main__':
    main()
