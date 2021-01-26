import requests
import pandas as pd


class User:
    def __init__(self, token):
        self.headers = requests.utils.default_headers()
        self.headers.update({'Authorization': 'token ' + token})
        self._data = {}
    
    def load(self, user):
        self._user = user
        
        data = requests.get('https://api.github.com/users/' + user, headers=self.headers)
        self._data = data.json()
    
        return self
    
    def get(self):
        return self._data
    
    def show(self):
        print("Information about user {}:".format(self._user))
        print("\tName: {}".format(self._data['name']))
        print("\tEmail: {}".format(self._data['email']))
        print("\tLocation: {}".format(self._data['location']))
        print("\tPublic repos: {}".format(self._data['public_repos']))
        print("\tPublic gists: {}".format(self._data['public_gists']))
        print("\tAbout: {}".format(self._data['bio']))
        
    


class Repository:
    def __init__(self, token):
        self._headers = requests.utils.default_headers()
        self._headers.update({'Authorization': 'token ' + token})
        
    
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
        url = user_data['repos_url']
        page_no = 1
        repos_data = []

        while (True):
            response = requests.get(url, headers=self._headers)
            response = response.json()
            repos_data = repos_data + response
            repos_fetched = len(response)
            if (repos_fetched == 30):
                page_no = page_no + 1
                url = user_data['repos_url'] + '?page=' + str(page_no)
            else:
                break

        self._dataframe = self.__dataframe__(repos_data)
                
        return self
        
    def get(self):
        return self._dataframe
    
    def save(self, file_path):
        self._dataframe.to_csv(file_path, index = False)
        return self
        

class Commit:
    def __init__(self, token):
        self._headers = requests.utils.default_headers()
        self._headers.update({'Authorization': 'token ' + token})
        self._data = {}

    def load(self, repos_df, user):
        self._repos_df = repos_df
        self._user = user
        
        self._commits_information = []
        for i in range(repos_df.shape[0]):
            url = repos_df.loc[i, 'Commits URL']
            page_no = 1
            while (True):
                response = self.__get_commit_data__(url)
                for commit in response:
                    if commit["author"] is not None:
                        if commit["author"]["login"] == user:
                            commit_data = self.__create_data__(commit, i, repos_df["Name"][i])
                            self._commits_information.append(commit_data)
                if (len(response) == 30):
                    page_no = page_no + 1
                    url = repos_df.loc[i, 'Commits URL'] + '?page=' + str(page_no)
                else:
                    break
        
        self._commits_df = pd.DataFrame(self._commits_information, columns = ['Repo Id', 'Commit Id', 'Date', 'Message'])
        return self
    
    def __get_commit_data__(self, url):
        response = requests.get(url, headers=self._headers)
        return response.json()
     
    def __create_data__(self, commit, index, repo):
#         print(commit["author"])
        commit_data = []
        commit_data.append(self._repos_df.loc[index, 'Id'])
        commit_data.append(commit['sha'])
        commit_data.append(commit['commit']['committer']['date'])
        commit_data.append(commit['commit']['message'])
        commit_data.append(repo)
       
        return commit_data
    
    
    def get(self):
        return self._commits_df

    def save(self, file_path):
        self._commits_df.to_csv(file_path, index = False)
        return self    



# def getData(repo):
#     data = []
#     data.append(repo['id'])
#     data.append(repo['name'])
#     data.append(repo['description'])
#     data.append(repo['created_at'])
#     data.append(repo['updated_at'])
#     data.append(repo['owner']['login'])
#     data.append(repo['license']['name'] if repo['license'] != None else None)
#     data.append(repo['has_wiki'])
#     data.append(repo['forks_count'])
#     data.append(repo['open_issues_count'])
#     data.append(repo['stargazers_count'])
#     data.append(repo['watchers_count'])
#     data.append(repo['url'])
#     data.append(repo['commits_url'].split("{")[0])
#     data.append(repo['url'] + '/languages')
    
#     return data


# def getReposDataframe(repos_data):
#     repos_information = []
#     for i, repo in enumerate(repos_data):
#         repos_information.append(getData(repo))

#     columns = ['Id', 'Name', 'Description', 'Created on', 'Updated on','Owner', 'License', 'Includes wiki', 
#                 'Forks count', 'Issues count', 'Stars count', 'Watchers count', 'Repo URL', 'Commits URL', 
#                 'Languages URL']
        
#     return pd.DataFrame(repos_information, columns=columns)