import os
import subprocess

from abc import abstractproperty
from wand.image import Image
from wand.color import Color

from base_page import BasePage


class ThumbnailPage(BasePage):
    def __init__(self):
        super().__init__()

    @abstractproperty
    def _folder(self):
        pass

    @abstractproperty
    def _ratio(self):
        pass

    def generate_thumbnail(self):
        fds = os.listdir(self._folder)
        fds = [x for x in fds if x[0] != '.']

        for fd in fds:
            sfds = os.listdir(os.path.join(self._folder, fd))
            sfds = [x for x in sfds if x[0] != '.']

            for sfd in sfds:
                f = os.path.join(self._folder, fd, sfd, 'report.pdf')
                if os.path.exists(f):
                    subprocess.call(['ls', f])
                else:
                    continue

                if os.path.exists(os.path.join(self._folder, fd, sfd, 'thumbnail.png')):
                    subprocess.call(['rm', os.path.join(self._folder, fd, sfd, 'thumbnail.png')])

                all_page = Image(filename=f)
                one_page = all_page.sequence[0]

                with Image(one_page) as pg:
                    pg.format = 'jpeg'
                    width = int(pg.width * self._ratio)
                    height = int(pg.height * self._ratio)
                    pg.resize(width, height)
                    pg.background_color = Color('white')
                    pg.alpha_channel = 'remove'
                    pg.compression_quality = 100
                    pg.save(filename=os.path.join(self._folder, fd, sfd, 'thumbnail.jpg'))
