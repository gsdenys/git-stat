import pandas as pd
import github.api as api

class User(api.Worker):

    def __init__(self, config):
        super().__init__(config)
    
    def load(self):
        self._user = super().getConf().getUser()
        
        user_url = "https://api.github.com/users/{}".format(self._user)
        columns = ['user', 'name', 'email', "location", "public_repos", 'public_gists', 'bio']
        
        self._data  = super().get(user_url)
        self._create_dataframe()
        
        return self
    
    def getData(self):
        return self._data
    
    def get(self):
        return self._dataframe
    
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
    
    def _create_dataframe(self):
        columns = ["User", "Name", "Email", "Location", "Repositories", "Gists", "Bio"]
        data = []
        
        data.append(self.getUser())
        data.append(self.getName())
        data.append(self.getEmail())
        data.append(self.getLocation())
        data.append(self.getNumRepos())
        data.append(self.getNumGists())
        data.append(self.getBio())
        
        self._dataframe = pd.DataFrame([data], columns=columns)
    
    def save(self):
        path = "{}/user_info_{}.csv".format(super().getConf().getPath(), super().getConf().getUser())
        self._dataframe.to_csv(path, index = False)
        
        print("Dataframe saved at: {}".format(path))
        
        return self
        
    def show(self):
        print("Information about user {}:".format(self.getUser()))
        print("\tName: {}".format(self.getName()))
        print("\tEmail: {}".format(self.getEmail()))
        print("\tLocation: {}".format(self.getLocation()))
        print("\tPublic repos: {}".format(self.getNumRepos()))
        print("\tPublic gists: {}".format(self.getNumGists()))
        print("\tAbout: {}".format(self.getBio()))
        
        return self