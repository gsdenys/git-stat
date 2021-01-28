import requests as req

class Worker:
    def __init__(self, token):
        self._headers = req.utils.default_headers()
        self._headers.update({'Authorization': 'token ' + token})

    def get(self, url):
        data = req.get(url, headers=self._headers)
        return data.json()