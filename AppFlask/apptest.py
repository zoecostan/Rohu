from flask import Flask, jsonify, request
import requests
#import tensorflow as tf
#from tensorflow.keras.models import Sequential
#from tensorflow.keras.layers import Dense

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
