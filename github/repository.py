import pandas as pd
import github.api as api

class Repository(api.Worker):

    def __init__(self):
        super().__init__()
    
    def __getData__(self, repo):
        data = []
        
        data.append(repo['id'])
        data.append(repo['name'])
        data.append(repo['description'])
        data.append(repo['created_at'])
        data.append(repo['updated_at'])
        data.append(repo['owner']['login'])
        data.append(repo['license']['name'] if repo['license'] != None else None)
        data.append(repo['has_wiki'])
        data.append(repo['forks_count'])
        data.append(repo['open_issues_count'])
        data.append(repo['stargazers_count'])
        data.append(repo['watchers_count'])
        data.append(repo['url'])
        data.append(repo['commits_url'].split("{")[0])
        data.append(repo['url'] + '/languages')
        
        return data
    
    def __dataframe__(self, repos_data):
        columns = [
            'Id', 'Name', 'Description', 'Created on', 'Updated on','Owner', 'License', 'Includes wiki', 
            'Forks count', 'Issues count', 'Stars count', 'Watchers count', 'Repo URL', 'Commits URL', 
            'Languages URL'
        ]
        
        repos_information = []
        for i, repo in enumerate(repos_data):
            repos_information.append(self.__getData__(repo))

        return pd.DataFrame(repos_information, columns=columns)
    
    def load(self, user_data):
        self._user_data = user_data
        
        url = self._user_data['repos_url']
        page_no = 1
        repos_data = []
        
        while (True):
            response = super().get(url)
            repos_data = repos_data + response
            repos_fetched = len(response)
            if (repos_fetched == 30):
                page_no = page_no + 1
                url = self._user_data['repos_url'] + '?page=' + str(page_no)
            else:
                break
        
        self._dataframe = self.__dataframe__(repos_data)
                
        return self
    
    def get(self):
        return self._dataframe
    
    def save(self):
        path = "{}/repos_info_{}.csv".format(super().getConf().getPath(), super().getConf().getUser())
        self._dataframe.to_csv(path, index = False)
        
        print("Dataframe saved at: {}".format(path))
        
        return self
        
        