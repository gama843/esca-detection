from flask import Flask, send_file
import folium

import numpy as np
from folium.plugins import HeatMapWithTime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

app = Flask(__name__, static_url_path='')

def initialize():
    cred = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://hack-a-toon.firebaseio.com/'
    })

initialize()

@app.route('/')
def hello():
    return "Hello World!"


if __name__ == '__main__':
#    initialize()
    app.run()


@app.route('/map')
def show_map():
    latitude = 48.445
    longitude = 21.687


    np.random.seed(3141592)
    initial_data = (
            np.random.normal(size=(300, 2)) * np.array([[0.003, 0.003]]) +
            np.array([[latitude, longitude]])
    )

    move_data = np.random.normal(size=(300, 2)) * 0.00001

    data = [(initial_data + move_data * i).tolist() for i in range(100)]

    weight = 1  # default value
    for time_entry in data:
        for row in time_entry:
            row.append(weight)

    mapa = folium.Map([48.726, 21.249], tiles='OpenStreetMap', zoom_start=14)
    hm = HeatMapWithTime(data, auto_play=True, max_opacity=0.8, radius=5)
    hm.add_to(mapa)

    ref = db.reference('vines')
    result = ref.get()
    for res in result:
        folium.Marker(
            location=[float(result[res]['latitude']), float(result[res]['longitude'])],
            popup=result[res]['class'],
            icon=folium.Icon(color='green')
        ).add_to(mapa)

    mapa.save('mapa.html')
    return send_file('mapa.html')






@app.route('/test')
def test():
    return "test route"
