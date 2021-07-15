import os
from fake_useragent import UserAgent
import requests


class WebUtil:
    ua = UserAgent()
    user_agent = {'user-agent': ua.random}

    @classmethod
    def save_img(cls, url, root, **kwargs):
        if url is None:
            return
        if len(kwargs) != 0:
            path = root + kwargs['name'] + '.' + url.split('.')[-1]
        else:
            path = root + url.split('/')[-1]

        try:
            if not os.path.exists(root):
                os.makedirs(root)
            if not os.path.exists(path):
                r = requests.get(url, headers=cls.user_agent)
                with open(path, 'wb') as f:
                    f.write(r.content)
                    f.close()
                    print("Done! Image saved!")
            else:
                print("Oops, image exists!")
        except requests.RequestException:
            print("Operation failed!")

    @classmethod
    def get_html(cls, url):
        try:
            r = requests.get(url, timeout=30, headers=cls.user_agent)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except requests.RequestException:
            return ""
