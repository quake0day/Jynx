from Pokemon import Pokemon
from datetime import datetime
from Location import Location
from Account import Account

username = raw_input('Enter a Account Username: ')
password = raw_input('Enter a Account Password: ')
no1 = Account(username = username, password = password, auth='ptc')
no1.save()

