from flask import Flask, jsonify, request, render_template, Response
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin

import search_engine
import json
import pandas as pd

app = Flask(__name__)
api = Api(app)

@app.route("/")
def start():
    return "Server running.."

@app.route("/search", methods=['POST'])
@cross_origin()
def search():
    body = request.get_json()
    print('Search input:')
    print(body)

    #Request body
    # {
    #     "searchTerm": "Counter-Strike",
    #     "boolOp" : 0,  # index of the list-item ['must', 'should', 'match']
    #     "filterOp" : 0,  # 0 for 'lt', 1 for 'gt'
    #      "categoryThreshold" : 3,
    #     "categoryFilter": 0, #index of the list-item ['price', 'rating', 'owners']
    #     "totalDocs": 10,
    #     "needSort" : 1,    #if sorting is needed, needSort =1 else needSort = 0
    #     "sortBy": ["PRICE"],       # required only if needSort = 1 ['PRICE', 'RATING', 'OWNERS']
    #     "isAscending":1,    # required only if needSort = 1
    #     "needFilter" : 1, #if filting is needed, needFilter =1 else needFilter = 0
    #     "categories": ['NAME', 'PRICE', 'RATING', 'SHORT_DESCRIPTION', 'OWNERS', 'TAGS'] # required only if needFilter = 1
    # }

    results = search_engine.search(body['searchTerm'], body['boolOp'], body['filterOp'], body['categoryThreshold'], body['categoryFilter'], body['totalDocs'])

    search_engine.tag_filter(results,True,[])

    print(len(results))

    if body['needSort'] == 1:
        results = search_engine.sorting(results, True, body['sortBy'], bool(body['isAscending']))

    if body['needFilter'] == 1:
        results = search_engine.filtering(results, True, body['categories'])

    feedback_list = ['Yes' for i in range(results.shape[0])] #default relevance feedback
    results['RELEVANT'] = feedback_list
    result = {"data": results }
    return json.dumps(result, default=lambda results: json.loads(results.to_json()))

@app.route("/sort", methods=['POST'])
@cross_origin()
def sort():
    body = request.get_json()
    print('Sort input:')
    print(body)

    # Request body
    # {   "docs":"{\"NAME\":{\"5\":\"AirMech Strike\",\"2\":\"Counter Agents\",\"3\":\"Counter Fight 3\",\"0\":\"Counter-Strike Nexon: Zombies\",\"1\":\"Counter-Strike: Global Offensive\",\"8\":\"Ember Strike\",\"7\":\"Fair Strike\",\"4\":\"Fantasy Strike\",\"6\":\"Fury Strike\",\"9\":\"Puzzle Strike\"},\"PRICE\":{\"5\":0.0,\"2\":0.0,\"3\":11.39,\"0\":0.0,\"1\":0.0,\"8\":0.0,\"7\":2.79,\"4\":14.99,\"6\":0.0,\"9\":10.99},\"RATING\":{\"5\":6200.0,\"2\":95.0,\"3\":4.0,\"0\":10003.0,\"1\":2242091.0,\"8\":639.0,\"7\":15.0,\"4\":190.0,\"6\":-6.0,\"9\":19.0},\"SHORT_DESCRIPTION\":{\"5\":\"AirMech\\u00ae Strike is a fast paced Action-RTS game that can be played online competitively or cooperatively. Earn Kudos and Experience in battle and unlock a wide collection of AirMechs and Units while you practice the perfect strategy to emerge victorious!\",\"2\":\"Counter Agents is a spy-themed, head-to-head multiplayer game where your objective is to sneak around guards, steal the briefcase, and make it to an exit point before your opponent!\",\"3\":\"Counter Fight is never dead! \\u201cCounter Fight 3\\u201d is a work simulation game where the player becomes a chef of a pizza store and provides meals to unique customers who appear one after another.\",\"0\":\"Counter-Strike Nexon: Zombies is a Free to Play MMOFPS offering competitive PvP and PvE action including content from the original Counter-Strike and all new game modes, maps, weapons, and hordes of Zombies!\",\"1\":\"Counter-Strike: Global Offensive (CS: GO) expands upon the team-based action gameplay that it pioneered when it was launched 19 years ago. CS: GO features new maps, characters, weapons, and game modes, and delivers updated versions of the classic CS content (de_dust2, etc.).\",\"8\":\"Fast head-to-head fighting like you\\u2019ve never seen.Welcome to Ember Strike. Join the first PVP fighter of its kind! Ember Strike is the perfect mix of speed and action with live, competitive, head-to-head battles.\",\"7\":\"Fair Strike is a game about brave pilots and their lethal celestial weapons fighting against terrorism and drug trafficking. So don't waste your time and jump into the cockpit of a modern attack helicopter and join a war against world terrorism. Your goal is simple - Kill them all!\",\"4\":\"A fighting game designed from the ground up to be so easy to control that even non-fighting game players can play it, yet deep enough to play in tournaments. Vibrant graphics and excellent online play.\",\"6\":\"Fury Strike is an 80s-themed 2.5D cel-shaded fighter game created by Full Sail University students in collaboration with Rooster Teeth.\",\"9\":\"Puzzle Strike is an online deckbuilding puzzle game from David Sirlin, lead designer of Puzzle Fighter HD Remix and creator of the Fantasy Strike universe. Improve your deck (of chips!) as the game unfolds and crush your opponents under a mountain of gems!\"},\"OWNERS\":{\"5\":1500000.0,\"2\":35000.0,\"3\":10000.0,\"0\":7500000.0,\"1\":75000000.0,\"8\":150000.0,\"7\":10000.0,\"4\":10000.0,\"6\":10000.0,\"9\":10000.0},\"TAGS\":{\"5\":\"action indie multiplayer strategy\",\"2\":\"indie casual\",\"3\":\"action indie casual simulation\",\"0\":\"action multiplayer singleplayer\",\"1\":\"action multiplayer strategy\",\"8\":\"action indie\",\"7\":\"action simulation\",\"4\":\"action indie\",\"6\":\"action\",\"9\":\"indie strategy\"}}",
    #     "sortBy": ["NAME"],
    #     "isAscending":1
    # }
    #categories = ['NAME', 'PRICE', 'RATING', 'SHORT_DESCRIPTION', 'OWNERS', 'TAGS']

    docs_json = json.loads(body['docs'])
    df = pd.DataFrame.from_dict(docs_json, orient="columns")

    # removing feedback column from previous results
    if 'RELEVANT' in df.keys():
        df.drop('RELEVANT', axis='columns', inplace=True)

    results = search_engine.sorting(df, True, body['sortBy'],body['isAscending'])

    feedback_list = ['Yes' for i in range(results.shape[0])]  # default relevance feedback
    results['RELEVANT'] = feedback_list

    result = {"data": results }
    return json.dumps(result, default=lambda results: json.loads(results.to_json()))

@app.route("/filter", methods=['POST'])
@cross_origin()
def filter():
    body = request.get_json()
    print('Filter input:')
    print(body)
    # Request body
    # {
    #     "docs": "{\"NAME\":{\"5\":\"AirMech Strike\",\"2\":\"Counter Agents\",\"3\":\"Counter Fight 3\",\"0\":\"Counter-Strike Nexon: Zombies\",\"1\":\"Counter-Strike: Global Offensive\",\"8\":\"Ember Strike\",\"7\":\"Fair Strike\",\"4\":\"Fantasy Strike\",\"6\":\"Fury Strike\",\"9\":\"Puzzle Strike\"},\"PRICE\":{\"5\":0.0,\"2\":0.0,\"3\":11.39,\"0\":0.0,\"1\":0.0,\"8\":0.0,\"7\":2.79,\"4\":14.99,\"6\":0.0,\"9\":10.99},\"RATING\":{\"5\":6200.0,\"2\":95.0,\"3\":4.0,\"0\":10003.0,\"1\":2242091.0,\"8\":639.0,\"7\":15.0,\"4\":190.0,\"6\":-6.0,\"9\":19.0},\"SHORT_DESCRIPTION\":{\"5\":\"AirMech\\u00ae Strike is a fast paced Action-RTS game that can be played online competitively or cooperatively. Earn Kudos and Experience in battle and unlock a wide collection of AirMechs and Units while you practice the perfect strategy to emerge victorious!\",\"2\":\"Counter Agents is a spy-themed, head-to-head multiplayer game where your objective is to sneak around guards, steal the briefcase, and make it to an exit point before your opponent!\",\"3\":\"Counter Fight is never dead! \\u201cCounter Fight 3\\u201d is a work simulation game where the player becomes a chef of a pizza store and provides meals to unique customers who appear one after another.\",\"0\":\"Counter-Strike Nexon: Zombies is a Free to Play MMOFPS offering competitive PvP and PvE action including content from the original Counter-Strike and all new game modes, maps, weapons, and hordes of Zombies!\",\"1\":\"Counter-Strike: Global Offensive (CS: GO) expands upon the team-based action gameplay that it pioneered when it was launched 19 years ago. CS: GO features new maps, characters, weapons, and game modes, and delivers updated versions of the classic CS content (de_dust2, etc.).\",\"8\":\"Fast head-to-head fighting like you\\u2019ve never seen.Welcome to Ember Strike. Join the first PVP fighter of its kind! Ember Strike is the perfect mix of speed and action with live, competitive, head-to-head battles.\",\"7\":\"Fair Strike is a game about brave pilots and their lethal celestial weapons fighting against terrorism and drug trafficking. So don't waste your time and jump into the cockpit of a modern attack helicopter and join a war against world terrorism. Your goal is simple - Kill them all!\",\"4\":\"A fighting game designed from the ground up to be so easy to control that even non-fighting game players can play it, yet deep enough to play in tournaments. Vibrant graphics and excellent online play.\",\"6\":\"Fury Strike is an 80s-themed 2.5D cel-shaded fighter game created by Full Sail University students in collaboration with Rooster Teeth.\",\"9\":\"Puzzle Strike is an online deckbuilding puzzle game from David Sirlin, lead designer of Puzzle Fighter HD Remix and creator of the Fantasy Strike universe. Improve your deck (of chips!) as the game unfolds and crush your opponents under a mountain of gems!\"},\"OWNERS\":{\"5\":1500000.0,\"2\":35000.0,\"3\":10000.0,\"0\":7500000.0,\"1\":75000000.0,\"8\":150000.0,\"7\":10000.0,\"4\":10000.0,\"6\":10000.0,\"9\":10000.0},\"TAGS\":{\"5\":\"action indie multiplayer strategy\",\"2\":\"indie casual\",\"3\":\"action indie casual simulation\",\"0\":\"action multiplayer singleplayer\",\"1\":\"action multiplayer strategy\",\"8\":\"action indie\",\"7\":\"action simulation\",\"4\":\"action indie\",\"6\":\"action\",\"9\":\"indie strategy\"}}",
    #     "sortBy": ["NAME"],
    #     "isAscending": 1
    #     }
    #categories = ['NAME', 'PRICE', 'RATING', 'SHORT_DESCRIPTION', 'OWNERS', 'TAGS']

    docs_json = json.loads(body['docs'])
    df = pd.DataFrame.from_dict(docs_json,orient="columns")

    # removing feedback column from previous results
    if 'RELEVANT' in df.keys():
        df.drop('RELEVANT',axis='columns', inplace=True)

    results = search_engine.filtering(df, True, body['categories'])

    feedback_list = ['Yes' for i in range(results.shape[0])]  # default relevance feedback
    results['RELEVANT'] = feedback_list

    result = {"data": results}
    return json.dumps(result, default=lambda results: json.loads(results.to_json()))

@app.route("/tagFilter", methods=['POST'])
@cross_origin()
def tag_filter():
    body = request.get_json()
    print('Filter input:')
    print(body)
    # Request body
    # {
    #     "docs": "{\"NAME\":{\"5\":\"AirMech Strike\",\"2\":\"Counter Agents\",\"3\":\"Counter Fight 3\",\"0\":\"Counter-Strike Nexon: Zombies\",\"1\":\"Counter-Strike: Global Offensive\",\"8\":\"Ember Strike\",\"7\":\"Fair Strike\",\"4\":\"Fantasy Strike\",\"6\":\"Fury Strike\",\"9\":\"Puzzle Strike\"},\"PRICE\":{\"5\":0.0,\"2\":0.0,\"3\":11.39,\"0\":0.0,\"1\":0.0,\"8\":0.0,\"7\":2.79,\"4\":14.99,\"6\":0.0,\"9\":10.99},\"RATING\":{\"5\":6200.0,\"2\":95.0,\"3\":4.0,\"0\":10003.0,\"1\":2242091.0,\"8\":639.0,\"7\":15.0,\"4\":190.0,\"6\":-6.0,\"9\":19.0},\"SHORT_DESCRIPTION\":{\"5\":\"AirMech\\u00ae Strike is a fast paced Action-RTS game that can be played online competitively or cooperatively. Earn Kudos and Experience in battle and unlock a wide collection of AirMechs and Units while you practice the perfect strategy to emerge victorious!\",\"2\":\"Counter Agents is a spy-themed, head-to-head multiplayer game where your objective is to sneak around guards, steal the briefcase, and make it to an exit point before your opponent!\",\"3\":\"Counter Fight is never dead! \\u201cCounter Fight 3\\u201d is a work simulation game where the player becomes a chef of a pizza store and provides meals to unique customers who appear one after another.\",\"0\":\"Counter-Strike Nexon: Zombies is a Free to Play MMOFPS offering competitive PvP and PvE action including content from the original Counter-Strike and all new game modes, maps, weapons, and hordes of Zombies!\",\"1\":\"Counter-Strike: Global Offensive (CS: GO) expands upon the team-based action gameplay that it pioneered when it was launched 19 years ago. CS: GO features new maps, characters, weapons, and game modes, and delivers updated versions of the classic CS content (de_dust2, etc.).\",\"8\":\"Fast head-to-head fighting like you\\u2019ve never seen.Welcome to Ember Strike. Join the first PVP fighter of its kind! Ember Strike is the perfect mix of speed and action with live, competitive, head-to-head battles.\",\"7\":\"Fair Strike is a game about brave pilots and their lethal celestial weapons fighting against terrorism and drug trafficking. So don't waste your time and jump into the cockpit of a modern attack helicopter and join a war against world terrorism. Your goal is simple - Kill them all!\",\"4\":\"A fighting game designed from the ground up to be so easy to control that even non-fighting game players can play it, yet deep enough to play in tournaments. Vibrant graphics and excellent online play.\",\"6\":\"Fury Strike is an 80s-themed 2.5D cel-shaded fighter game created by Full Sail University students in collaboration with Rooster Teeth.\",\"9\":\"Puzzle Strike is an online deckbuilding puzzle game from David Sirlin, lead designer of Puzzle Fighter HD Remix and creator of the Fantasy Strike universe. Improve your deck (of chips!) as the game unfolds and crush your opponents under a mountain of gems!\"},\"OWNERS\":{\"5\":1500000.0,\"2\":35000.0,\"3\":10000.0,\"0\":7500000.0,\"1\":75000000.0,\"8\":150000.0,\"7\":10000.0,\"4\":10000.0,\"6\":10000.0,\"9\":10000.0},\"TAGS\":{\"5\":\"action indie multiplayer strategy\",\"2\":\"indie casual\",\"3\":\"action indie casual simulation\",\"0\":\"action multiplayer singleplayer\",\"1\":\"action multiplayer strategy\",\"8\":\"action indie\",\"7\":\"action simulation\",\"4\":\"action indie\",\"6\":\"action\",\"9\":\"indie strategy\"}}",
    #     "tags": ["action"],
    #     }

    docs_json = json.loads(body['docs'])
    df = pd.DataFrame.from_dict(docs_json,orient="columns")

    # removing feedback column from previous results
    if 'RELEVANT' in df.keys():
        df.drop('RELEVANT',axis='columns', inplace=True)

    results = search_engine.tag_filter(df, True, body['tags'])

    feedback_list = ['Yes' for i in range(results.shape[0])]  # default relevance feedback
    results['RELEVANT'] = feedback_list

    result = {"data": results}
    return json.dumps(result, default=lambda results: json.loads(results.to_json()))

@app.route("/feedback", methods=['POST'])
@cross_origin()
def feedback():
    body = request.get_json()
    feedback_list = body['Results']
    search_engine.evaluate(feedback_list)
    return Response(status=200)


if __name__ == '__main__':
    search_engine.main()
    app.run(debug=True, use_reloader = False, threaded= False)


