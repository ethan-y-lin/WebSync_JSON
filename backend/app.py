import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler
import pandas as pd

# ROOT_PATH for linking with all your files. 
# Feel free to use a config.py or settings.py with a global export variable
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..",os.curdir))

# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Specify the path to the JSON file relative to the current script
json_file_path = os.path.join(current_directory, 'novel_info.json')

def getKeyInfo(data,key):
    titles = []
    for d in data:
        titles.append(d[key])
    return titles
# Assuming your JSON data is stored in a file named 'init.json'
with open(json_file_path, 'r') as file:
    data = json.load(file)
    titles = getKeyInfo(data,'titles')
    descriptions = getKeyInfo(data,'description')

app = Flask(__name__)
CORS(app)

def json_search(query):
    matches = []
    for i in range (len(titles)):
        if query.lower() in titles[i][0].lower() and query != "":
            matches.append({'title': titles[i],'descr':descriptions[i]})
    return matches

@app.route("/")
def home():
    return render_template('base.html',title="sample html")

@app.route("/episodes")
def episodes_search():
    text = request.args.get("title")
    return json_search(text)

if 'DB_NAME' not in os.environ:
    app.run(debug=True,host="0.0.0.0",port=5000)