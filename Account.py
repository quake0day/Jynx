import sys, os
import ConfigParser
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from flask_mongoalchemy import MongoAlchemy
from flask_mongoalchemy import BaseQuery


cf = ConfigParser.ConfigParser()
cf.read("./config.ini")
db_host = cf.get("baseconf", "host")
db_name = cf.get("accountconf", "db_name")

app = Flask(__name__)
app.config['MONGOALCHEMY_DATABASE'] = db_name
app.config['MONGOALCHEMY_SERVER'] = db_host
db = MongoAlchemy(app)



class Account(db.Document):
    username = db.StringField()
    password = db.StringField()
    auth = db.StringField()
    isUsed = db.BooleanField()

    def setInfo(self, username, password, auth):
        self.username = username
        self.password = password
        self.auth = auth 
        self.isUsed = False 
        return 


    def getInfo(self):
        return self.username, self.password, self.auth 

    def isUsed(self):
        return self.isUsed == True


    def set(self):
        self.isUsed = True 
        return

    def reset(self):
        self.isUsed = False
        return 