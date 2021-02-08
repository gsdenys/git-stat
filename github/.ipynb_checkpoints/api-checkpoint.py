import configparser
import requests as req

class Worker:
    def __init__(self):
        self._conf = Config()
        
        self._headers = req.utils.default_headers()
        self._headers.update({'Authorization': 'token ' + self._conf.getToken()})

    def get(self, url):
        data = req.get(url, headers=self._headers)
        return data.json()

    def getConf(self):
        return self._conf


class Config:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self._user = config['github']['user']
        self._token = config['github']['token']
        self._path = config['base']['path']
        
    def getUser(self):
        return self._user
    
    def getToken(self):
        return self._token
    
    def getPath(self):
        return self._path
