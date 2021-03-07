import base64

import requests

from data.config import IMGBBKEY


class ImgbbLoader:

    def upload_photo(self, filename):
        with open(
                fr'.\photos\{filename}.jpg',
                "rb") as file:  # TODO DANGER rewrite paths
            url = "https://api.imgbb.com/1/upload"
            payload = {
                "key": IMGBBKEY,
                "image": base64.b64encode(file.read()),
            }
            res = requests.post(url, payload)
            url = res.json()
            url = url.get('data')
            url = url.get('url')
            return url
