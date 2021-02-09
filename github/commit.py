import pandas as pd
import github.api as api

class Commit(api.Worker):

    def __init__(self):
        super().__init__()
    
    def load(self, repos_df):
        self._repos_df = repos_df
        self._user = super().getConf().getUser()
                
        self._commits_information = []
        for i in range(repos_df.shape[0]):
            url = repos_df.loc[i, 'Commits URL']
            page_no = 1
            while (True):
                response = super().get(url)
                for commit in response:
                    if commit["author"] is not None:
                        if len(commit["author"]) > 0 and commit["author"]["login"] == self._user:
                            commit_data = self.__create_data__(commit, i, repos_df["Name"][i])
                            self._commits_information.append(commit_data)
                if (len(response) == 30):
                    page_no = page_no + 1
                    url = repos_df.loc[i, 'Commits URL'] + '?page=' + str(page_no)
                else:
                    break
        
        self._commits_df = pd.DataFrame(
            self._commits_information, 
            columns = ['Repo Id', 'Commit Id', 'Date', 'Message', "Repository"]
        )
        
        return self
     
    def __create_data__(self, commit, index, repo):
        commit_data = []
        commit_data.append(self._repos_df.loc[index, 'Id'])
        commit_data.append(commit['sha'])
        commit_data.append(commit['commit']['committer']['date'])
        commit_data.append(commit['commit']['message'])
        commit_data.append(repo)
       
        return commit_data
    
    
    def get(self):
        return self._commits_df

    def save(self):
        path = "{}/commits_info_{}.csv".format(super().getConf().getPath(), super().getConf().getUser())
        self._commits_df.to_csv(path, index = False)
        
        print("Dataframe saved at: {}".format(path))
        
        return self
    