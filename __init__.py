from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')
@app.route('/contact/')
def MaPremiereAPI():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")
  @app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

# Route pour extraire les commits par minute
@app.route('/commits/')
def commits_per_minute():
    # Utiliser l'API de GitHub pour obtenir les données sur les commits
    response = requests.get('https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits')
    commits_data = response.json()

    # Initialiser un dictionnaire pour stocker le nombre de commits par minute
    commits_per_minute = {}

    # Parcourir les données des commits
    for commit in commits_data:
        date_string = commit['commit']['author']['date'] # Obtenir la date du commit
        minute = extract_minutes(date_string).json['minutes'] # Extraire les minutes de la date du commit
        commits_per_minute[minute] = commits_per_minute.get(minute, 0) + 1 # Incrémenter le nombre de commits pour cette minute

    return jsonify(commits_per_minute)


  
if __name__ == "__main__":
  app.run(debug=True)
