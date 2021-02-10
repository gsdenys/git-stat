import requests as req
from config import Config

class GitWorker:
    """ Worker class to helps implementation of github API actions """

    def __init__(self, config):
        """Default Builder

        Args:
            config (Config): The configuratin object
        """
        
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



