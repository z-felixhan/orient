from flask import Flask, json, jsonify, request
import requests
import yaml

app = Flask(__name__)

# Load config
with open('config.yml') as c:
    config = yaml.load(c, Loader=yaml.FullLoader)
    OPENWEATHERMAP_API_KEY = config['OPENWEATHERMAP']['API_KEY']


@app.route('/')
def index():
    return '<h1>ORIENT API</h1>'


@app.route('/openweathermap/weather', methods=['GET'])
# https://openweathermap.org/current
def openweathermap_weather():
    if request.args.get('q'):
        return json.loads(requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={request.args.get('q')}&appid={OPENWEATHERMAP_API_KEY}").content)
