from datetime import datetime
from elasticsearch import Elasticsearch, helpers
import csv
import pandas as pd

steamAppsIndex = 'steamapps'


def init():
    es = Elasticsearch()
    return es


def preprocess(datasetPath, tagsPath):

    fields = ['appid', 'name', 'positive_ratings',
              'negative_ratings', 'owners', 'price']
    df = pd.read_csv(datasetPath, index_col='appid', usecols=fields)

    tags = ['action', 'indie', 'adventure', 'multiplayer', 'singleplayer',
            'casual', 'rpg', 'strategy', 'open_world', 'simulation']

    fields = ['appid'] + tags
    tagsDb = pd.read_csv(tagsPath, index_col='appid', usecols=fields)

    tagsDb['tagCount'] = tagsDb.sum(axis=1, skipna=True)

    # assign boolean value for each tag (ignoring appid field)
    userAgreementTreshold = 0.1
    for tag in tags:
        df[tag] = tagsDb[tag] > userAgreementTreshold * tagsDb['tagCount']

    # join positive and negative ratings into single score
    df['rating'] = df['positive_ratings'] - df['negative_ratings']
    df = df.drop(['positive_ratings', 'negative_ratings'], axis=1)

    # clean owners into single number (center of band)
    df['owners'] = (df['owners'].str.split('-').str[0].astype(int) +
                    df['owners'].str.split('-').str[1].astype(int)) // 2
    print(tagsDb)
    print(df)


def indexSteamApps(es, datasetPath):
    print(f'indexing csv {datasetPath}...')

    # erase previous index
    es.indices.delete(index=steamAppsIndex, ignore=[
                      400, 404])

    with open(datasetPath, encoding='utf8', errors='replace') as f:
        reader = csv.DictReader(f)
        response = helpers.bulk(es, reader, index=steamAppsIndex)
        print("RESPONSE:", response)

    es.indices.refresh(index=steamAppsIndex)


def query(es, settings):
    total_docs = 12
    result = es.search(index=steamAppsIndex, body={
        "query": settings}, size=total_docs)

    print("Got %d Hits:" % result['hits']['total']['value'])
    for hit in result['hits']['hits']:
        print(f'{hit["_source"]["name"]}')
        print('================')
    return result


def main():
    # connect to Elasticsearch server
    es = init()

    # preprocess data
    datasetPath = 'data/steam.csv'
    tagsPath = 'data/steamspy_tag_data.csv'
    preprocess(datasetPath, tagsPath)

    # index/update steamapps from csv file
    indexSteamApps(es, datasetPath)

    # test querry
    settings = {"match": {'name': 'Counter-Strike'}}
    result = query(es, settings)

    # TODO: sort, filter and display result

    print('exit')


if __name__ == "__main__":
    # execute only if run as a script
    main()
