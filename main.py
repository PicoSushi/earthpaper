#!/usr/bin/env python3
from tempfile import mkstemp
from random import choice
from binascii import a2b_base64
import subprocess

import click
import requests

IDLIST_LOC = "./IDLIST"    # ???
WALLPAPER_CMD = ['feh', '--bg-fill']    # Command to set wallpaper.


def fetch_image(image_id):
    image_url = 'https://www.gstatic.com/prettyearth/assets/data/v2/' + image_id + '.json'
    resp = requests.get(image_url)
    result = resp.json()
    image_bin = a2b_base64(str(result['dataUri'].split(',')[1]))
    fname = mkstemp('-earth-{}.jpg'.format(image_id))[1]
    with open(fname, 'wb') as f:
        f.write(image_bin)
    return fname


@click.command()
@click.option('--set-wallpaper', type=bool, default=False, help='Sets fetched image as wallpaper.')
def main(set_wallpaper):
    with open(IDLIST_LOC) as f:
        image_ids = f.readlines()
    image_id = choice(image_ids).strip()
    file_name = fetch_image(image_id)
    if set_wallpaper:
        # check if wallpaper command exists
        if len(subprocess.run(['whereis', WALLPAPER_CMD[0]], stdout=subprocess.PIPE).stdout.decode('utf8').split()
               ) <= 1:
            raise Exception("Need {} command to set wallpaper!".format(WALLPAPER_CMD[0]))
        subprocess.run(WALLPAPER_CMD + [file_name])


if __name__ == '__main__':
    main()
