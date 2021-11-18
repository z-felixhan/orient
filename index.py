from flask import Flask, json, jsonify, request
from flask_cors import CORS
import os
import requests
import yaml

app = Flask(__name__)
dir = os.path.dirname(os.path.realpath(__file__))
CORS(app)

# Load config
with open(dir + '/config.yml') as c:
    config = yaml.load(c, Loader=yaml.FullLoader)
    OPENWEATHERMAP_API_KEY = config['OPENWEATHERMAP']['API_KEY']
    GC_GSTRATE_API_KEY = config['GC']['GSTRATE']['API_KEY']


@app.route('/')
def index():
    return '<h1>ORIENT API</h1>'


@app.route('/openweathermap/weather', methods=['GET'])
# https://openweathermap.org/current
def openweathermap_weather():
    if request.args.get('q'):
        return json.loads(requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={request.args.get('q')}&appid={OPENWEATHERMAP_API_KEY}").content)


@app.route("/gc/gstrate", methods=['GET'])
# https://cra-arc.api.canada.ca/en/detail?api=GSTRate
def gc_gstrate():
    return json.loads(requests.get(f"https://gstrate-cra-arc.api.canada.ca/ebci/ghnf/api/ext/v1/rates", headers={"user-key": GC_GSTRATE_API_KEY}).content)
