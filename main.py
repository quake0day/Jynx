#import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import csv
import os
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from Pokemon import Pokemon
# configuration
DEBUG = False
app = Flask(__name__)
# you can set key as config
app.config['GOOGLEMAPS_KEY'] = "AIzaSyDaxIPVJlz-F6Lry-tuXiZjwD_uglj5kdw"
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
GoogleMaps(app)



@app.route("/")
def index():
    res = Pokemon.query.all()
    res = res[::-1]
    res = res[:100]
    markers_ = []
    for pokemon in res:
        lat, lng = pokemon.get_loc() 
        marker = {}
        marker['icon'] = pokemon.get_thumbnail_url()
        marker['lat'] = lat
        marker['lng'] = lng
        marker['infobox'] = "Time:"+str(pokemon.get_time())
        markers_.append(marker)
    #print markers_

    mymap = Map(

        identifier="view-side",
        lat=43.0007,
        lng=-78.782873
    )
    sndmap = Map(
        zoom = 15,
        style = "height:500px; margin: auto; width: 95%;border: 1px solid black;padding: 10px;",
        identifier="sndmap",
        lat=43.0007,
        lng=-78.782873,
        markers=markers_
    )
    
    
    return render_template('index.html', info = res, mymap=mymap, sndmap=sndmap)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(host= '0.0.0.0')

            
