import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

def count_commit(repos, commits):
    cc = pd.DataFrame(
        pd.merge(
            repos, 
            commits, 
            left_on='Id', 
            right_on='Repo Id', 
            how = 'left'
        )
        .groupby('Id')
        .size()
        .reset_index()
    )
    
    cc.columns = ['Id', 'Commits count']
    
    return cc


def show(repos, commits):
    print("Total repos till date: {}".format(repos.shape[0]))
    print("Total commits till date: {}".format(commits.shape[0]))
    print("Total starts till date: {}".format(repos['Stars count'].sum()))
    print("Total Watchers till date: {}".format(repos['Watchers count'].sum()))

    
def draw(x, y, x_label, y_label, title):
    plt.figure(figsize = (20, 12))
    sns.barplot(x=x, y=y)
    plt.xticks(rotation = 90)
    plt.xlabel(x_label, fontsize = 16)
    plt.ylabel(y_label, fontsize = 16)
    plt.title(title, fontsize = 16)