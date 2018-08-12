from tempfile import mkstemp
from random import choice
from binascii import a2b_base64

import requests

IDLIST_LOC = "./IDLIST"


def fetch_image(image_id):
    image_url = 'https://www.gstatic.com/prettyearth/assets/data/v2/' + image_id + '.json'
    resp = requests.get(image_url)
    result = resp.json()
    image_bin = a2b_base64(str(result['dataUri'].split(',')[1]))
    fname = mkstemp('-earth.jpg')[1]
    with open(fname, 'wb') as f:
        f.write(image_bin)
    return fname


def main():
    with open(IDLIST_LOC) as f:
        image_ids = f.readlines()
    image_id = choice(image_ids).strip()
    file_name = fetch_image(image_id)
    print(file_name)


if __name__ == '__main__':
    main()
