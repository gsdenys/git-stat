import requests
import pandas as pd
import matplotlib.pyplot as plt

columns = ['name', 'fork', 'created_at', 'updated_at', 'pushed_at', 'size', 'stargazers_count',
 'watchers_count', 'language', 'has_issues', 'has_projects', 'has_downloads', 'has_wiki',
 'has_pages', 'forks_count', 'archived', 'disabled', 'open_issues_count', 'forks',
 'open_issues', 'watchers', 'default_branch']

url = "https://api.github.com/users/{user}/repos" 


def _jsonToDataframe(json_data):
    df = pd.DataFrame(json_data, columns=columns)

    df['created_at'] = pd.to_datetime(df['created_at'])
    df['updated_at'] = pd.to_datetime(df['updated_at'])
    df['pushed_at'] = pd.to_datetime(df['pushed_at'])

    df['year'] = pd.DatetimeIndex(df['created_at']).year

    return df


def getRepos(user):
    url_repo = url.replace("{user}", user)
    repos = requests.get(url_repo)

    return _jsonToDataframe(repos.json())

def creationFromYear(dataframe):
    language = dataframe.groupby(["language", "year"])["language"].count().reset_index(name="count")
    language_year_count = language.pivot(index='year', columns='language', values='count')

    language_year_count = language_year_count.fillna(0)

    return language_year_count

def creationFromYear(dataframe):
    language = dataframe.groupby(["language", "year"])["language"].count().reset_index(name="count")
    language_year_count = language.pivot(index='year', columns='language', values='count')

    language_year_count = language_year_count.fillna(0)

    return language_year_count


def printCreationByYear(user):
    df = getRepos(user)
    creation_from_year = creationFromYear(df)
    creation_from_year.plot(kind="area", figsize=(20,10), title="Criação de Repositórios por Linguagem por Ano")