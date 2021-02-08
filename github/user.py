import pandas as pd
import github.api as api


class User(api.Worker):

    def __init__(self):
        super().__init__()
    
    def load(self):
        self._user = super().getConf().getUser()
        
        user_url = "https://api.github.com/users/{}".format(self._user)
        columns = ['user', 'name', 'email', "location", "public_repos", 'public_gists', 'bio']
        
        self._data  = super().get(user_url)
        
        return self
    
    def get(self):
        return self._data
    
    def getUser(self):
        return self._user
    
    def getName(self):
        return self._data['name']
    
    def getEmail(self):
        return self._data['email']
    
    def getLocation(self):
        return self._data['location']
    
    def getNumRepos(self):
        return self._data['public_repos']
    
    def getNumGists(self):
        return self._data['public_gists']

    def getBio(self):
        return self._data['bio']
    
    def show(self):
        print("Information about user {}:".format(self.getUser()))
        print("\tName: {}".format(self.getName()))
        print("\tEmail: {}".format(self.getEmail()))
        print("\tLocation: {}".format(self.getLocation()))
        print("\tPublic repos: {}".format(self.getNumRepos()))
        print("\tPublic gists: {}".format(self.getNumGists()))
        print("\tAbout: {}".format(self.getBio()))