# pip install pandas
# pip install elasticsearch
# using Python 3.9.0
# make sure to run elasticsearch.bat

from timeit import default_timer as timer
import pandas as pd
import csv
from elasticsearch import Elasticsearch, helpers
import re as re


steamAppsIndex = 'steamapps'


def init():
    es = Elasticsearch()
    return es


def preprocess(steamtPath, tagsPath, descriptionPath, outputPath):
    print('preprocessing dataset...')
    start = timer()

    fields = ['appid', 'name', 'positive_ratings',
              'negative_ratings', 'owners', 'price']
    df = pd.read_csv(steamtPath, index_col='appid', usecols=fields)

    # clean owners into single number (center of band)
    df['owners'] = (df['owners'].str.split('-').str[0].astype(int) +
                    df['owners'].str.split('-').str[1].astype(int)) // 2

    # join positive and negative ratings into single score
    df['rating'] = df['positive_ratings'] - df['negative_ratings']
    df = df.drop(['positive_ratings', 'negative_ratings'], axis=1)

    tags = ['action', 'indie', 'adventure', 'multiplayer', 'singleplayer',
            'casual', 'rpg', 'strategy', 'open_world', 'simulation']

    fields = ['appid'] + tags
    tagsDf = pd.read_csv(tagsPath, index_col='appid', usecols=fields)

    tagsDf['tagCount'] = tagsDf.sum(axis=1, skipna=True)

    # assign boolean value for each tag (ignoring appid field)
    userAgreementTreshold = 0.1
    for tag in tags:
        df[tag] = tagsDf[tag] > userAgreementTreshold * tagsDf['tagCount']

    # get game descriptions
    fields = ['steam_appid', 'detailed_description',
              'about_the_game', 'short_description']
    descDf = pd.read_csv(
        descriptionPath, index_col='steam_appid', usecols=fields)

    # remove html tags
    df['about_the_game'] = descDf['about_the_game'].apply(
        lambda x: re.sub('<.*?>', '', x))
    df['short_description'] = descDf['short_description'].apply(
        lambda x: re.sub('<.*?>', '', x))
    df['detailed_description'] = descDf['detailed_description'].apply(
        lambda x: re.sub('<.*?>', '', x))

    print(df)
    print(f'finished preprocessing in {timer()-start}s')
    df.to_csv(path_or_buf=outputPath)


def indexSteamApps(es, datasetPath):
    print(f'indexing csv {datasetPath}...')

    # erase previous index
    es.indices.delete(index=steamAppsIndex, ignore=[
                      400, 404])
    start = timer()

    with open(datasetPath, encoding='utf8', errors='replace') as f:
        reader = csv.DictReader(f)
        #response = helpers.bulk(es, reader, index=steamAppsIndex)
        for success, info in helpers.parallel_bulk(es, reader, index=steamAppsIndex):
            if not success:
                print(f'A document failed: {info}')

    print(f'finished indexing in {timer()-start}s')

    es.indices.refresh(index=steamAppsIndex)


def query(es, settings):
    print('')
    print(settings)
    start = timer()

    total_docs = 8
    result = es.search(index=steamAppsIndex, body={
        "query": settings}, size=total_docs)

    print('')
    print(f"Got {result['hits']['total']['value']} Hits in {timer()-start}s:")

    print('')
    for hit in result['hits']['hits']:
        print(f'{hit["_source"]["name"]}')
        print(f'${hit["_source"]["price"]} rating: {hit["_source"]["rating"]}')
        print(f'{hit["_source"]["short_description"]}')
        print('================')
    return result


def main():
    # connect to Elasticsearch server
    es = init()

    # preprocess data
    steamtPath = 'data/steam.csv'
    tagsPath = 'data/steamspy_tag_data.csv'
    descriptionPath = 'data/steam_description_data.csv'
    datasetPath = 'temp/dataset.csv'
    preprocess(steamtPath, tagsPath, descriptionPath, outputPath=datasetPath)

    # index/update steamapps from csv file
    indexSteamApps(es, datasetPath)

    # test querry
    settings = {"match": {'name': 'Worms'}}
    result = query(es, settings)

    # TODO: sort, filter and display result

    print('exit')


if __name__ == "__main__":
    # execute only if run as a script
    main()
