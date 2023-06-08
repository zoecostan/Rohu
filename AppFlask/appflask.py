from flask import Flask, jsonify, request
import requests
from flask_sqlalchemy import SQLAlchemy
import json

import mysql.connector
#import tensorflow as tf
#from tensorflow.keras.models import Sequential
#from tensorflow.keras.layers import Dense

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://zoe:rohu@localhost/airports'
db = SQLAlchemy(app)

class Airport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50))
    name = db.Column(db.String(200))
    cityCode = db.Column(db.String(50))
    cityName = db.Column(db.String(200))
    countryName = db.Column(db.String(200))
    countryCode = db.Column(db.String(200))
    timezone = db.Column(db.String(8))
    lat = db.Column(db.String(32))
    lon = db.Column(db.String(32))
    numAirports = db.Column(db.Integer)
    city = db.Column(db.Enum('true', 'false'))

# Carga el modelo de TensorFlow entrenado
#model = tf.keras.models.load_model('modelo.h5')

@app.route('/')
def hello():
    return 'Ajouter longitude et latitude à la requête afin d observer des résultats.'

@app.route('/forecast/<lat>/<lng>')
def process_forecast(lat, lng):
    api_key = 'b1723b95bdb54629c30ac93f1bfe77c2'
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&units=metric&appid={api_key}'

    response = requests.get(url)
    forecast = response.json()
    #weather_description = forecast["weather"][0]["description"]
    #input_data = [1 if "rain" in weather_description else 0]
    #prediction = model.predict([input_data])
   
    #if prediction[0] >= 0.5:
    #    result = "El drone debe aterrizar."
    #else:
    #    result = "El drone puede seguir volando."
   
    return jsonify({'result': forecast})

#La fonction process_forecast est définie en tant que point de terminaison (endpoint) de votre application Flask avec la route /forecast/<lat>/<lng>.
#Lorsqu'une requête est effectuée à cette route avec des valeurs de latitude et de longitude spécifiées, par exemple /forecast/48.8566/2.3522, Flask récupère ces valeurs et les passe en tant qu'arguments à la fonction process_forecast.
#À l'intérieur de la fonction process_forecast, les valeurs de latitude et de longitude sont utilisées pour construire l'URL de l'API OpenWeatherMap.
#Ensuite, une requête GET est effectuée à l'URL construite en utilisant requests.get(url).
#La réponse de l'API est obtenue en appelant .json() sur l'objet de réponse, ce qui renvoie les données de prévision au format JSON.
#Enfin, les données de prévision sont renvoyées en tant que réponse JSON à l'appelant de la requête.

@app.route('/check_airport/<latitude>/<longitude>', methods=['GET'])
def check_airport(latitude, longitude):
    latitude = float(latitude)
    longitude = float(longitude)


    # Interroger la base de données pour trouver les aéroports à moins de 8 km
    airports = Airport.query.filter(
        Airport.lat.between(latitude - 0.072, latitude + 0.072),
        Airport.lon.between(longitude - 0.072, longitude + 0.072)
    ).all()

    if airports:
        message = "Veuillez vous éloigner de l'aéroport."
    else:
        message = "Vous êtes à une distance sécuritaire de l'aéroport."

    response = {
        'message': message
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
