#import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import csv
import os
from flask.ext.mongoalchemy import MongoAlchemy
from flask.ext.mongoalchemy import BaseQuery
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from pokemon_id_name import get_id2name_table
# configuration
DEBUG = False
app = Flask(__name__)
app.config['MONGOALCHEMY_DATABASE'] = 'pokemon'
# you can set key as config
app.config['GOOGLEMAPS_KEY'] = "AIzaSyDaxIPVJlz-F6Lry-tuXiZjwD_uglj5kdw"
db = MongoAlchemy(app)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
GoogleMaps(app)


class Pokemon(db.Document):
    pid = db.IntField()
    lat = db.FloatField()
    lng = db.FloatField()
    report_time = db.DateTimeField()
    id2name = get_id2name_table()
    encounter_id = db.StringField()

    def get_img_url(self):
        return url_for('static', filename='img/')+str(self.pid)+".png"

    def get_thumbnail_url(self):
        return url_for('static', filename='thumbnail/')+str(self.pid)+".png"

    def get_pid(self):
            return self.pid

    def get_name(self):
        return self.id2name[self.pid]

    def get_loc(self):
        return self.lat, self.lng

    def get_loc_display(self):
        return str(self.lat) + ", " + str(self.lng)

    def get_time(self):
        return self.report_time

    def get_encounter_id(self):
        return self.encounter_id



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
        style = "height:500px;width:800px;margin:10;",
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
    app.run(host= '10.0.1.19')

            
