import sys, os
import ConfigParser
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from flask_mongoalchemy import MongoAlchemy
from flask_mongoalchemy import BaseQuery
from dbConnection import getDb

db = getDb('locationconf')


class Location(db.Document):
    lat = db.FloatField()
    lng = db.FloatField()
    isOn = db.IntField(default=0)

    def setLocation(self, lat, lng):
        self.lat = lat
        self.lng = lng 
        self.isOn = 0

    def getLocation(self):
        return self.lat, self.lng

    def getOn(self):
        return self.isOn

    def setOn(self):
        self.isOn = 1
        return 

    def setOff(self):
        self.isOn = 0
        return 