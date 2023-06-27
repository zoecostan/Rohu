import tensorflow as tf
import requests

# URL and Key API
url = "https://api.openweathermap.org/data/2.5/weather"
api_key = "b1723b95bdb54629c30ac93f1bfe77c2"

# Parameters for the request
lat = 40.464878  # Example latitude
lon = 17.253235  # Example longitude
params = {
    "lat": lat,
    "lon": lon,
    "appid": api_key,
    "units": "metric"
}

# Make the request to the API
response = requests.get(url, params=params)
data = response.json()

# Obtaining relevant data for the model
temperature = data["main"]["temp"]
humidity = data["main"]["humidity"]
wind_speed = data["wind"]["speed"]
cloudiness = data["clouds"]["all"]

# Define input and output data
input_data = [temperature, humidity, wind_speed, cloudiness]
output_data = 1 if "rain" in [weather["main"] for weather in data["weather"]] else 0

# Create the model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(16, activation='relu', input_shape=(4,)),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
input_data = tf.expand_dims(input_data, 0)  # Agregar dimensión de lote (batch dimension)
output_data = tf.expand_dims(output_data, 0)
model.fit(input_data, output_data, epochs=10)


# Save the model
model.save('model.h5')
