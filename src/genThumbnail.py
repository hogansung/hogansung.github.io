import os
import subprocess
from wand.image import Image
from wand.color import Color

targets = [
    {
        'target_folder': '../project/undergrad',
        'ratio': 0.6,
    },
    {
        'target_folder': '../project/graduate',
        'ratio': 0.3,
    },
    {
        'target_folder': '../research',
        'ratio': 1.0,
    },
]

def main():
    for target in targets:
        target_folder = target['target_folder']
        ratio = target['ratio']

        fds = os.listdir(target_folder)
        fds = filter(lambda x: x[0] != '.', fds)
        
        for fd in fds:
            sfds = os.listdir(os.path.join(target_folder, fd))
            sfds = filter(lambda x: x[0] != '.', sfds)

            for sfd in sfds:
                f = os.path.join(target_folder, fd, sfd, 'report.pdf')
                if os.path.exists(f):
                    subprocess.call(['ls', f])
                else:
                    continue

                if os.path.exists(os.path.join(target_folder, fd, sfd, 'thumbnail.png')):
                    subprocess.call(['rm', os.path.join(target_folder, fd, sfd, 'thumbnail.png')])

                all_page = Image(filename=f)
                one_page = all_page.sequence[0]

                with Image(one_page) as pg:
                    pg.format = 'jpeg'
                    width = long(pg.width * ratio)
                    height = long(pg.height * ratio)
                    pg.resize(width, height)
                    pg.background_color = Color('white')
                    pg.alpha_channel = 'remove'
                    pg.compression_quality = 100
                    pg.save(filename=os.path.join(target_folder, fd, sfd, 'thumbnail.jpg'))


if __name__ == '__main__':
    main()
