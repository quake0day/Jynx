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





# def connect_db():
#     return sqlite3.connect(app.config['DATABASE']

# @app.before_request
# def before_request():
#     # g.db = connect_db()

# @app.teardown_request
# def teardown_request(exception):
#     db = getattr(g, 'db', None)
#     if db is not None:
#         db.close(

# def id2name(id):
#     with open('./data/pokemon.csv', 'rb') as f:
#         reader = csv.reader(f)
#         your_list = list(reader)
#         print your_list

# class ID2Name(db.Document):
#     pid = db.IntField()
#     name = db.StringField()

#     def get_name(self):
#         return self.name 

#     def get_pid(self):
#         return self.pid 

class Pokemon(db.Document):
    pid = db.IntField()
    lat = db.FloatField()
    lng = db.FloatField()
    report_time = db.DateTimeField()
    id2name = get_id2name_table()

    def get_img_url(self):
        return url_for('static', filename='img/')+str(self.pid)+".png"

    def get_thumbnail_url(self):
        return url_for('static', filename='thumbnail/')+str(self.pid)+".png"

    def get_pid(self):
            return self.pid

    def get_name(self):
        return self.id2name[self.pid]

    def get_loc(self):
        return (self.lat, self.lng)

    def get_time(self):
        return (self.report_time)



@app.route("/")
def index():
    #cur = g.db.execute('select * from entries order by year desc')
    #entries = [dict(id=row[0], type=row[1], title=row[2], author=row[3], confname=row[4], urlpaper=row[5], urlslides=row[6], urlcite=row[7], cite=row[8], place=row[9], year=row[10], text=row[11]) for row in cur.fetchall()]
    #entries = []
    #pokemon_info = db.pokemon.find()
    # Initialize the extension
    res = Pokemon.query.all()
    markers_ = []
    for pokemon in res:
        lat, lng = pokemon.get_loc() 
        marker = {}
        marker['icon'] = pokemon.get_thumbnail_url()
        marker['lat'] = lat
        marker['lng'] = lng
        marker['infobox'] = "Time:"+str(pokemon.get_time())
        markers_.append(marker)
    print markers_

    mymap = Map(

        identifier="view-side",
        lat=10.01,
        lng=10.101
    )
    sndmap = Map(
        style = "height:500px;width:800px;margin:10;",
        identifier="sndmap",
        lat=10.01,
        lng=10.101,
        markers=markers_
    )
    
    
    return render_template('index.html', info = res, mymap=mymap, sndmap=sndmap)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)

            
