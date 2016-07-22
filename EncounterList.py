import sys, os
import ConfigParser
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from flask_mongoalchemy import MongoAlchemy
from flask_mongoalchemy import BaseQuery
from dbConnection import getDb

db = getDb('baseconf')

class EncounterList(db.Document):
    ID = db.StringField()

    def getID(self):
        return self.ID
