import sys, os
import ConfigParser
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from flask_mongoalchemy import MongoAlchemy
from flask_mongoalchemy import BaseQuery


cf = ConfigParser.ConfigParser()
cf.read("./config.ini")
db_host = cf.get("baseconf", "host")
db_name = cf.get("locationconf", "db_name")

app = Flask(__name__)
app.config['MONGOALCHEMY_DATABASE'] = db_name
app.config['MONGOALCHEMY_SERVER'] = db_host
db = MongoAlchemy(app)


class Location(db.Document):
    lat = db.FloatField()
    lng = db.FloatField()
    isOn = db.BooleanField()

    def setLocation(self, lat, lng):
        self.lat = lat
        self.lng = lng 
        self.isOn = False

    def getLocation(self):
        return self.lat, self.lng

    def isOn(self):
        return self.isOn == True

    def setOn(self):
        self.isOn = True
        return 

    def setOff(self):
        self.isOn = False
        return 