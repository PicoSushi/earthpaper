from tempfile import mkstemp
from random import choice
import requests
from binascii import a2b_base64


def fetch_image(image_id):
    image_url = 'https://www.gstatic.com/prettyearth/assets/data/v2/' + image_id + '.json'
    resp = requests.get(image_url)
    result = resp.json()
    image_bin = a2b_base64(str(result['dataUri'].split(',')[1]))
    fname = mkstemp('-earth.jpg')
    with open(fname, 'wb') as f:
        f.write(image_bin)
    return fname


if __name__ == '__main__':
    with open('./IDLIST') as f:
        image_ids = f.readlines()
    image_id = choice(image_ids).strip()
    file_name = fetch_image(image_id)
