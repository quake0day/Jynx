from Pokemon import Pokemon
from datetime import datetime
from Location import Location
from Account import Account

lat = raw_input('Enter a Lat: ')
lng = raw_input('Enter a Lng: ')
no5 = Location(lat = float(lat), lng = float(lng))
no5.save()
