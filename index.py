from flask import Flask, json, jsonify, request
from flask_cors import CORS
import data
import os
import requests
import yaml

app = Flask(__name__)
dir = os.path.dirname(os.path.realpath(__file__))
CORS(app)

# Load config
with open(dir + '/config.yml') as c:
    config = yaml.load(c, Loader=yaml.FullLoader)
    GC_GSTRATE_API_KEY = config['GC']['GSTRATE']['API_KEY']
    OPENWEATHERMAP_API_KEY = config['OPENWEATHERMAP']['API_KEY']
    RIOT_API_KEY = config['RIOT']['API_KEY']

# Load data
NOC = data.NOC


@app.route('/')
def index():
    return '<h1 style="text-align: center">ORIENT API</h1>'


### WRAPPERS ###

@app.route('/gc/gstrate', methods=['GET'])
# https://cra-arc.api.canada.ca/en/detail?api=GSTRate
def gc_gstrate():
    return json.loads(requests.get(f'https://gstrate-cra-arc.api.canada.ca/ebci/ghnf/api/ext/v1/rates', headers={'user-key': GC_GSTRATE_API_KEY}).content)


@app.route('/openweathermap/weather', methods=['GET'])
# https://openweathermap.org/current
def openweathermap_weather():
    if request.args.get('q'):
        return json.loads(requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={request.args.get("q")}&appid={OPENWEATHERMAP_API_KEY}').content)


# https://developer.riotgames.com/apis
@app.route('/riotgames/lol/summoner/v4/summoners/<string:region>/by-name/<string:summonerName>', methods=['GET'])
def riotgames_lol_get_summoner_by_summoner_name(region, summonerName):
    return json.loads(requests.get(f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}', headers={'X-Riot-Token': RIOT_API_KEY}).content)


### CUSTOM ###

@app.route('/noc/v1/2016')
def gc_noc_2016():
    return jsonify(NOC)
