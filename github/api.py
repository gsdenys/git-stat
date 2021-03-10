import requests as req
# from config import Config

class Worker:
    """ Worker class to helps implementation of github API actions """

    def __init__(self, config):
        """Default Builder

        Args:
            config (Config): The configuratin object
        """
        
        self._config = config
        
        # Create the HTTP requeste header
        self._headers = req.utils.default_headers()
        self._headers.update({'Authorization': 'token ' + config.getToken()})

    def get(self, url):
        """Function to perform a HTTP GET request through any URL.

        Args:
            url (str): The http URL

        Returns:
            JSON: The json-encoded content of a response, if any.
        """
        data = req.get(url, headers=self._headers)
        return data.json()

    def getConf(self):
        return self._config

