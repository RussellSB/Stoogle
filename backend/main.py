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
    print(f'finished preprocessing in {timer() - start}s')
    df.to_csv(path_or_buf=outputPath)


def indexSteamApps(es, datasetPath):
    print(f'indexing csv {datasetPath}...')

    # erase previous index
    es.indices.delete(index=steamAppsIndex, ignore=[
        400, 404])
    start = timer()

    with open(datasetPath, encoding='utf8', errors='replace') as f:
        reader = csv.DictReader(f)
        # response = helpers.bulk(es, reader, index=steamAppsIndex)
        for success, info in helpers.parallel_bulk(es, reader, index=steamAppsIndex):
            if not success:
                print(f'A document failed: {info}')

    print(f'finished indexing in {timer() - start}s')

    es.indices.refresh(index=steamAppsIndex)


def query(es, settings, total_docs):
    print('')
    print(settings)
    start = timer()

    result = es.search(index=steamAppsIndex, body={"query": settings}, size=total_docs)  # returns a dictionary

    print('')
    print(f"Got {result['hits']['total']['value']} Hits in {timer() - start}s:")

    print('')

    # lists for data storage
    # text based
    name = []
    short_description = []
    detailed_description = []
    about_the_game = []

    # numerics
    price = []
    rating = []
    # appid = []
    owners = []

    # tags
    tags = []

    for hit in result['hits']['hits']:  # extract entries from a list

        tag_temp = []
        # print entries and add to the relevant lists declared above
        # print(f'{hit["_source"]}')
        name.append(hit["_source"]["name"])
        price.append(float(hit["_source"]["price"]))
        rating.append(float(hit["_source"]["rating"]))
        # appid.append(float(hit["_source"]["appid"]))
        owners.append(float(hit["_source"]["owners"]))
        short_description.append(hit["_source"]["short_description"])
        detailed_description.append(hit["_source"]["detailed_description"])
        about_the_game.append((hit["_source"]["about_the_game"]))

        # get tags and put them into a string
        if (hit["_source"]["action"]) == 'True':
            tag_temp.append('action')
        if (hit["_source"]["indie"]) == 'True':
            tag_temp.append('indie')
        if (hit["_source"]["adventure"]) == 'True':
            tag_temp.append('adventure')
        if (hit["_source"]["multiplayer"]) == 'True':
            tag_temp.append('multiplayer')
        if (hit["_source"]["singleplayer"]) == 'True':
            tag_temp.append('singleplayer')
        if (hit["_source"]["casual"]) == 'True':
            tag_temp.append('casual')
        if (hit["_source"]["rpg"]) == 'True':
            tag_temp.append('rpg')
        if (hit["_source"]["strategy"]) == 'True':
            tag_temp.append('strategy')
        if (hit["_source"]["open_world"]) == 'True':
            tag_temp.append('open_world')
        if (hit["_source"]["simulation"]) == 'True':
            tag_temp.append('simulation')
        tags.append(' '.join([str(item) for item in tag_temp]))

    dict = {'NAME': name, 'PRICE': price, 'RATING': rating, 'SHORT_DESCRIPTION': short_description, 'OWNERS': owners,
            'TAGS': tags}  # store lists into a dictionary
    result = pd.DataFrame(dict)  # output dictionary as a dataframe and return the dataframe

    return result


def sorting(df, sorting_criteria, ascending):
    """
    :param df: an input dataframe
    :param sorting_criteria: the parameters by which you wish to sort
    :param ascending: boolean value
    :return: sorted dataframe
    """
    df = df.sort_values(by=sorting_criteria, ascending=ascending)
    return df


def filtering(df, items):
    """
    :param df: an input dataframe
    :param items: the columns you would like to keep
    :return: dataframe with specified columns
    """
    df = df.filter(items=items)
    return df


def substring_search(df, category, substring):
    """
    :param df: input data frame
    :param category: the column you would like to search a string for
    :param substring: the string to check for
    :return: dataframe with entries containing specified string in specified column
    """
    df = df[df[category].str.contains(substring)]
    return df


def print_the_data(result, sorted_data, filtered_data, data_with_string):
    pd.set_option('max_columns', 6)  # this is to print out all columns
    print('============')
    print('Sorted Data')
    print('============')
    print(sorted_data)
    print('=============')
    print('Filtered Data')
    print('=============')
    print(filtered_data)
    print('=================')
    print('Data With String')
    print('=================')
    print(data_with_string)


def generate_settings(selection_index, title, bool_op_index, categories_index, filter_operation_index, threshold):
    # test query
    bool_op = ['must', 'should', 'match']
    filter_operation = ['lt', 'gt']
    categories = ['price', 'rating', 'owners']

    print(type(selection_index))
    selection_index = selection_index % 3

    if selection_index == 0:
        # print('MATCH: ', title)
        settings = {"match": {'name': title}}  # match operator
    elif selection_index == 1:
        # print('BOOL: ', bool_op[bool_op_index], title)
        settings = {'bool': {bool_op[bool_op_index]: [{'match': {'name': title}}]}}  # bool must operator
    elif selection_index == 2:
        # print('BOOL: ', bool_op[bool_op_index], title, categories[categories_index], filter_operation[filter_operation_index], threshold)
        settings = {'bool': {bool_op[bool_op_index]: {'match': {'name': title}}, "filter": {"range": {
            categories[categories_index]: {filter_operation[filter_operation_index]: threshold}}}}}  # filter operation
    else:
        print('No Instruction Found')
    return settings


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

    categories = ['NAME', 'PRICE', 'RATING', 'SHORT_DESCRIPTION', 'OWNERS', 'TAGS']

    # test query
    selection_index = int(input("Enter selection_index :"))  # 4
    title = str(input("Enter title : "))  # 'Counter-Strike'
    bool_op_index = int(input("Enter Desired Boolean Operation : "))  # 0
    categories_index = int(input("Enter Category Index : "))  # 0
    filter_operation_index = int(input("Enter Filter Operation Index : "))  # 0
    threshold = float(input("Enter Threshold : "))  # 3.0
    total_docs = int(input("Enter Number of Documents Desired : "))  # 3.0

    settings = generate_settings(selection_index, title, bool_op_index, categories_index, filter_operation_index,
                                 threshold)
    result = query(es, settings, total_docs)

    # TODO: sort, filter and display result
    ascending = bool(input("Ascending (True) or Descending (False) Order : "))  # False
    print('Categories: ', result.columns)
    sorting_criteria_index = int(input("Enter Sorting Criteria Index : "))  # 0
    sorting_criteria = [categories[sorting_criteria_index]]
    sorted_data = sorting(result, sorting_criteria, ascending)

    print('Categories: ', sorted_data.columns)
    category_to_remove_index = int(input("Enter Category Index to Remove :"))  # 4
    categories.remove(categories[category_to_remove_index])
    filtered_data = filtering(df=sorted_data, items=categories)

    print('Categories: ', filtered_data.columns)
    category = categories[int(input("Enter Category Index to search for Substring :"))]
    substring = float(input("Enter word to search for : "))  # simulation
    data_with_string = substring_search(filtered_data, category, substring)

    print_the_data(result, sorted_data, filtered_data, data_with_string)

    print('exit')


if __name__ == "__main__":
    # execute only if run as a script
    main()
