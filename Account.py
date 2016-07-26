import sys, os
import ConfigParser
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from flask_mongoalchemy import MongoAlchemy
from flask_mongoalchemy import BaseQuery
from dbConnection import getDb

db = getDb('accountconf')


class Account(db.Document):
    username = db.StringField()
    password = db.StringField()
    auth = db.StringField()
    isUsed = db.IntField(default=0)

    def setInfo(self, username, password, auth):
        self.username = username
        self.password = password
        self.auth = auth 
        self.isUsed = 0
        return 0


    def getInfo(self):
        return self.username, self.password, self.auth 

    def getUsed(self):
        return self.isUsed 

    def disable(self):
        self.isUsed = 2
        return 0

    def set(self):
        self.isUsed = 1
        return 0

    def reset(self):
        self.isUsed = 0
        return 0