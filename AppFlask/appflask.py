from flask import Flask, jsonify, request
import requests
from flask_sqlalchemy import SQLAlchemy
import math
import numpy as np

import tensorflow as tf
from tensorflow.keras.models import load_model

from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "Rohu2023"  # Change this!
jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://zoecostan:565399@localhost:3306/meetdrone4'

db = SQLAlchemy(app)

class Airport(db.Model):
    __tablename__ = 'airports'
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

# Load the trained tf model
model = tf.keras.models.load_model('model.h5')

# Annexe function
def haversineGreatCircleDistance(latitudeFrom, longitudeFrom, latitudeTo, longitudeTo):
    # convert degrés to radians
    earthRadius = 6371000
    latFrom = math.radians(latitudeFrom)
    lonFrom = math.radians(longitudeFrom)
    latTo = math.radians(latitudeTo)
    lonTo = math.radians(longitudeTo)

    latDelta = latTo - latFrom
    lonDelta = lonTo - lonFrom

    angle = 2 * math.asin(math.sqrt(math.pow(math.sin(latDelta / 2), 2) +
                     math.cos(latFrom) * math.cos(latTo) * math.pow(math.sin(lonDelta / 2), 2)))
    distance = angle * earthRadius

    return round(distance, 2)

# Route pour l'authentification
@app.route('/auth', methods=['POST'])
def authenticate():
    username = request.json.get('username')
    password = request.json.get('password')

    # Vérification des informations d'identification
    if username == "zoecostan" and password == "565399":
        # Génération du jeton JWT
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message="Invalid username or password"), 401

# ...

# Basic request without parameters
@app.route('/')
def hello():
    return 'Add parameters to the request (lon, lat)'

# All previsions (geofence and meteo including tensorflow)
# http://localhost:5000/allinfo/lat/long
@app.route('/allinfo/<latitude>/<longitude>', methods=['GET'])
@jwt_required
def all_info(latitude, longitude):
    latitude = float(latitude)
    longitude = float(longitude)

    api_key = 'b1723b95bdb54629c30ac93f1bfe77c2'
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=metric&appid={api_key}'

    responseforecast = requests.get(url)
    forecast = responseforecast.json()

    # Assumer une valeur de 1 pour "rain" dans weather_description, sinon 0
    input_data = [0, 0, 0, 0]

    # Récupérer les paramètres avec des valeurs par défaut de None
    temperature = request.args.get('temperature')
    humidity = request.args.get('humidity')
    wind_speed = request.args.get('wind_speed')
    cloudiness = request.args.get('cloudiness')

    # Convertir les valeurs en float si elles ne sont pas None
    if temperature is not None:
        input_data[0] = float(temperature)
    if humidity is not None:
        input_data[1] = float(humidity)
    if wind_speed is not None:
        input_data[2] = float(wind_speed)
    if cloudiness is not None:
        input_data[3] = float(cloudiness)

    # Créer un tableau NumPy avec les valeurs d'entrée
    input_data = np.array(input_data, dtype=np.float32)

    # Assurez-vous que les données d'entrée ont la bonne forme
    input_data = np.expand_dims(input_data, axis=0)

    # Prédiction du modèle
    prediction = model.predict(input_data)[0]
    if prediction >= 0.5:
        resulttf = "El drone debe aterrizar."
    else:
        resulttf = "El drone puede seguir volando."


    # Interroger la base de données pour trouver les aéroports
    airports = Airport.query.all()

    geofence = {'value': False}  # Initialiser la variable geofence

    # Vérifier la distance entre chaque aéroport et les coordonnées fournies
    for airport in airports:
        airport_latitude = float(airport.lat)
        airport_longitude = float(airport.lon)
        distance = haversineGreatCircleDistance(latitude, longitude, airport_latitude, airport_longitude)
        
        if distance <= 12000:  # Vérifier si la distance est inférieure ou égale à 8000 mètres (8 km)
            geofence['value'] = True
            geofence['airport'] = {
                'name': airport.name,
                'latitude': airport_latitude,
                'longitude': airport_longitude,
                'distance': f"{distance}m"
            }            
            break
    else:
        geofence['value'] = False

    # Créer le dictionnaire contenant forecast et response
    result = {
        'forecast': forecast,
        'geofence': geofence,
        'decision': resulttf
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
