import sys, os
import ConfigParser
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from flask_mongoalchemy import MongoAlchemy
from flask_mongoalchemy import BaseQuery
from pokemon_id_name import get_id2name_table


cf = ConfigParser.ConfigParser()
cf.read("./config.ini")
db_host = cf.get("baseconf", "host")
db_name = cf.get("baseconf", "db_name")

app = Flask(__name__)
app.config['MONGOALCHEMY_DATABASE'] = db_name
app.config['MONGOALCHEMY_SERVER'] = db_host
db = MongoAlchemy(app)

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
        return self.report_time.strftime('%Y-%m-%d %H:%M:%S')

    def get_encounter_id(self):
        return self.encounter_id