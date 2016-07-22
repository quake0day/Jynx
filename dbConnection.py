import sys, os
import ConfigParser
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from flask_mongoalchemy import MongoAlchemy
from flask_mongoalchemy import BaseQuery


def getDb(conf_name):
    cf = ConfigParser.ConfigParser()
    cf.read("./config.ini")
    db_host = cf.get("baseconf", "host")
    db_name = cf.get(conf_name, "db_name")

    app = Flask(__name__)
    app.config['MONGOALCHEMY_DATABASE'] = db_name
    app.config['MONGOALCHEMY_SERVER'] = db_host
    db = MongoAlchemy(app)
    return db
