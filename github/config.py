from configparser import ConfigParser

class Config:
    """ The class responsible to load the configuration data.  """

    def __init__(self):
        """ Default Builder """
        # initialize the data estracgion from  config.ini
        config = ConfigParser()
        config.read('config.ini')

        # Extract data
        self._user = config['github']['user']
        self._token = config['github']['token']
        self._path = config['base']['path']
        
    def getUser(self) -> str:
        """ Get configurated user
        
        Returns:
            str: The configurated username
        """
        return self._user
    
    def getToken(self) -> str:
        """ Get configurated Token 

        Returns:
            str: The configurated github token
        """
        return self._token
    
    def getPath(self) -> str:
        """ Get the base path to store and read the data

        Returns:
            str: The configurated path
        """
        return self._path
    
    def __get_path__(self, file_prefix) -> str:
        """Private function to create the file path

        Args:
            file_prefix (str): the file prefix

        Returns:
            str: the file path
        """
        return "{}/{}_info_{}.csv".format(
            self.getPath(), 
            file_prefix, 
            self.getUser()
        )

    def getUserPath(self) -> str:
        """Get the file path to user data.

        Returns:
            str: user info file path
        """
        return self.__get_path__("user") 
    
    def getRepoPath(self) -> str:
        """Get the file path to repository data information

        Returns:
            str: repository info file path
        """
        return self.__get_path__("user") 
    
    def getCommitPath(self) -> str:
        """Get the file path to commit data information

        Returns:
            str: commit info file path
        """
        return self.__get_path__("commits") 
    
    def getLanguagePath(self) -> str:
        """Get the file path to language data information

        Returns:
            str: language info file path
        """
        return self.__get_path__("commits") 
