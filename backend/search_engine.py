# pip install pandas
# pip install elasticsearch
# using Python 3.9.0
# make sure to run elasticsearch.bat

from timeit import default_timer as timer
import pandas as pd
import csv
from elasticsearch import Elasticsearch, helpers
import re as re
from collections import Counter
import math
import os.path
import matplotlib.pyplot as plt

steamAppsIndex = 'steamapps'
es = Elasticsearch()

column_headers = ['query','q-precision','p@cutoff','s-precision','DCG','hits','time-lag']
df_queries = pd.DataFrame(columns = column_headers)

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

    results = []

    total_hits = 0
    total_time = 0

    for setting in settings:
        result = es.search(index=steamAppsIndex, body={"query": setting}, size=total_docs//3)  # returns a dictionary

        print('')
        print(f"Got {result['hits']['total']['value']} Hits in {timer() - start}s:")
        total_hits += result['hits']['total']['value']
        total_time += (timer() - start)

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
        results.append(result)

    result = pd.concat(results, ignore_index=True) # put all dataframes together
    result = result.drop_duplicates() # get rid of all duplicates

    return result

def sorting(df, en, sorting_criteria, ascending):
    """
    :param df: an input dataframe
    :param sorting_criteria: the parameters by which you wish to sort
    :param ascending: boolean value
    :return: sorted dataframe
    """

    if en:
        df = df.sort_values(by=sorting_criteria, ascending=ascending, ignore_index=True)
    return df

def filtering(df, en, threshold, index):
    """
    :param df: an input dataframe
    :param items: the columns you would like to keep
    :return: dataframe with specified columns
    """
    categories = ['PRICE', 'RATING', 'OWNERS']
    if en:
        df = df[df[categories[index]] <= threshold]
        df_queries.iloc[-1, 0] = df_queries.iloc[-1, 0]+' '+categories[index]+'<='+str(threshold)
    return df

def tag_filter(df, en, tags):
    """
    :param df: input data frame
    :param category: the column you would like to search a string for
    :param substring: the string to check for
    :return: dataframe with entries containing specified string in specified column
    """
    if en:
        for tag in tags:
          df = df[df['TAGS'].str.contains(tag)]
        if len(tags)> 0:
            df_queries.iloc[-1, 0] = df_queries.iloc[-1, 0] + ' tags = ' + str(tags)
    return df

# def print_the_data(result, sorted_data, filtered_data, data_with_string):
#     pd.set_option('max_columns', 6)  # this is to print out all columns
#     print('============')
#     print('Sorted Data')
#     print('============')
#     print(sorted_data)
#     print('=============')
#     print('Filtered Data')
#     print('=============')
#     print(filtered_data)
#     print('=================')
#     print('Data With String')
#     print('=================')
#     print(data_with_string)

def generate_settings(text):

    settings0 = {'bool': {'should': {'match': {'name': text}}}}
    settings1 = {'bool': {'should': {'match': {'tags': text}}}}
    settings2 = {'bool': {'should': {'match': {'short_description': text}}}}

    settings = [settings0, settings1, settings2]
    
    global df_queries
    df_queries = df_queries.append(
        {'query': str(settings), 'q-precision': 0, 'p@cutoff': 0, 's-precision': 0, 'DCG': 0,
         'hits': 0, 'time-lag': 0},
        ignore_index=True)

    return settings
              
def main():
    # preprocess data
    steamtPath = 'data/steam.csv'
    tagsPath = 'data/steamspy_tag_data.csv'
    descriptionPath = 'data/steam_description_data.csv'
    datasetPath = 'temp/dataset.csv'
    preprocess(steamtPath, tagsPath, descriptionPath, outputPath=datasetPath)

    # index/update steamapps from csv file
    indexSteamApps(es, datasetPath)

def search(searchTerm, totalDocs):
    print('====NEW SEARCH =====')

    settings = generate_settings(searchTerm)
    results =query(es, settings, totalDocs)

    global df_queries
    df_queries.iloc[-1, 5] = len(results)
    return results

def evaluate(feedback_list = [], time_lag= 0.0):
    print('====EVALUATION =====')
    global df_queries


    # Query-specific precision
    count_dict = Counter(feedback_list)
    q_precision = count_dict['Yes']/len(feedback_list)
    q_precision = round(q_precision,2)
    print('Q-precision:'+str(q_precision))
    df_queries.iloc[-1, 1] = q_precision

    # System-wide precision
    if os.path.exists('evaluation\df_queries.csv'):
        df = pd.read_csv('evaluation\df_queries.csv')
        s_precision = df['q-precision'].sum()/df.shape[0]
        s_precision = round(s_precision,2)
        print('S-precision:' + str(s_precision))
        df_queries.iloc[-1, 3]  = s_precision

    # Precision at cut-off
    p_cutoffs = []
    for i in range(1,11):
        count_dict_p_cutoff = Counter(feedback_list[:i])
        p_cutoff = count_dict_p_cutoff['Yes'] / i
        p_cutoffs.append(round(p_cutoff,2))
        print('precision @ cutoff '+str(i)+': ' + str(p_cutoff))
        df_queries.iloc[-1, 2] = str(p_cutoffs)

    # Discounted Cumulative Gain
    DCG_list =[]
    p = len(feedback_list) # number of documents retrieved
    feedback_list_int = [1 if f == 'Yes' else 0 for f in feedback_list]
    for r in range(1, p):
        DCG = feedback_list_int[0]
        for i in range(1, r):
            DCG += (pow(2,feedback_list_int[i])-1)/(math.log(1+i))
        DCG = round(DCG,3)
        DCG_list.append(DCG)
    df_queries.iloc[-1, 4] = str(DCG_list)
    print('DCG:' + str(DCG_list))

    df_queries.iloc[-1, 6] = time_lag

    if os.path.exists('evaluation\df_queries.csv'):
        df = pd.read_csv('evaluation\df_queries.csv')
        df.append(df_queries.tail(1)) # Only append last row of df_queries
        df_queries.tail(1).to_csv('evaluation\df_queries.csv', mode='a', header=False, index=False)
    else:
        df_queries.to_csv(r'evaluation\df_queries.csv', index=False)
        df = df_queries

    #code to plot p@cutoff curves
    x = [i+1 for i in range(10)]
    plt.title('Precision at cutoff for each query')
    plt.xlabel('Cutoff')
    plt.ylabel('Precision')
    for i in range(df.shape[0]):
        y = str2list(df.iloc[i, 2])
        plt.plot(x, y, label = "Query"+str(i+1))

    plt.legend(loc='best')
    plt.savefig('evaluation\plot'+str(df.shape[0])+'.png')
    plt.pause(5)
    plt.clf() # clear plot

def str2list(str_data):
    str_data = str_data.strip('"')
    str_data = str_data.strip('[')
    str_data = str_data.strip(']')
    str_data = str_data.strip(',')
    y = []
    y = str_data.split(',')
    y = [float(i) for i in y]
    return y

if __name__ == "__search_engine__":
    # execute only if run as a script
    main()
