import pandas as pd
import github.api as api

class Languages(api.Worker):

    def __init__(self):
        super().__init__()
    
    def load(self, repos_df):
        self._repos_df = repos_df
        #self._user = super().getConf().getUser()
        
        self._languages_information = []
        for i in range(repos_df.shape[0]):
            url = repos_df.loc[i, 'Languages URL']
            page_no = 1
            while (True):
                response = super().get(url)
                for lang in response:
                    language = self.__create_data__(lang, i, repos_df["Name"][i], response[lang])
                    self._languages_information.append(language)

                if (len(response) == 30):
                    page_no = page_no + 1
                    url = repos_df.loc[i, 'Languages URL'] + '?page=' + str(page_no)
                else:
                    break
        
        self._languages_df = pd.DataFrame(
            self._languages_information, 
            columns = ['Repo Id', 'Language', 'Size', 'Repo Name']
        )
        
        return self
     
    def __create_data__(self, lang, index, repo, value):
        language_data = []
        language_data.append(self._repos_df.loc[index, 'Id'])
        language_data.append(lang)
        language_data.append(value)
        language_data.append(repo)
       
        return language_data
    
    
    def get(self):
        return self._languages_df

    def save(self):
        path = super().getConf().getLanguagePath()
        self._languages_df.to_csv(path, index = False)
        
        print("Dataframe saved at: {}".format(path))
        
        return self
    