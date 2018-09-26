from flask import Flask, send_file
import folium

import numpy as np
from folium.plugins import HeatMapWithTime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

app = Flask(__name__, static_url_path='')

def initialize():
   if (not len(firebase_admin._apps)):
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
    app.run(debug=True,host='35.205.127.36',port=5000)


@app.route('/map')
def show_map():
    latitude = 48.445
    longitude = 21.687


    np.random.seed(3141592)
    initial_data = (
            np.random.normal(size=(300, 2)) * np.array([[0.003, 0.003]]) +
            np.array([[latitude, longitude]])
    )

    move_data = np.random.normal(size=(300, 2)) * 0.00003

    data = [((np.delete(initial_data, np.s_[0:i * 5], axis=0)) +
            (np.delete(move_data, np.s_[0:i * 5], axis=0)) * i).tolist() for i in range(1, 61)]

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
        folium.Circle(
            location=[float(result[res]['latitude']), float(result[res]['longitude'])],
            radius=20,
	    color='crimson',
	    fill=True,
	    popup=result[res]['class']
        ).add_to(mapa)

    mapa.save('mapa.html')
    return send_file('mapa.html')






@app.route('/test')
def test():
    return "test route"
