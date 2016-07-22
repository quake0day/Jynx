#!/usr/bin/env python
"""
pgoapi - Pokemon Go API
Copyright (c) 2016 tjado <https://github.com/tejado>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.

Author: tjado <https://github.com/tejado>
"""

import os
import re
import json
import struct
import logging
import requests
import argparse
import collections
import pickle


from pgoapi import PGoApi
from pgoapi.utilities import f2i, h2f

from google.protobuf.internal import encoder
from geopy.geocoders import GoogleV3
from s2sphere import CellId, LatLng

# for parsing the pokemon id to its name 
# can be disabled
#import pykemon

# for searching only
import geopy
from geopy.distance import VincentyDistance
from time import sleep

# for saving to database

from Pokemon import Pokemon
from Account import Account
from Location import Location
from datetime import datetime



log = logging.getLogger(__name__)

def get_pos_by_name(location_name):
    geolocator = GoogleV3()
    loc = geolocator.geocode(location_name)

    log.info('Your given location: %s', loc.address.encode('utf-8'))
    log.info('lat/long/alt: %s %s %s', loc.latitude, loc.longitude, loc.altitude)

    return (loc.latitude, loc.longitude, loc.altitude)

def get_cellid(lat, long):
    origin = CellId.from_lat_lng(LatLng.from_degrees(lat, long)).parent(15)
    walk = [origin.id()]

    # 10 before and 10 after
    next = origin.next()
    prev = origin.prev()
    for i in range(10):
        walk.append(prev.id())
        walk.append(next.id())
        next = next.next()
        prev = prev.prev()
    return ''.join(map(encode, sorted(walk)))

def encode(cellid):
    output = []
    encoder._VarintEncoder()(output.append, cellid)
    return ''.join(output)

def init_config():
    try:
        account = Account.query.filter(Account.isUsed == False).first_or_404()
        username, password, auth = account.getInfo() 
        location = Location.query.filter(Location.isOn == False).first_or_404()
        lat, lng = location.getLocation()
    except Exception, e:
        print e 
        

    # parser = argparse.ArgumentParser()
    # config_file = "config.json"


    # # If config file exists, load variables from json
    # load   = {}
    # if os.path.isfile(config_file):
    #     with open(config_file) as data:
    #         load.update(json.load(data))

    # # Read passed in Arguments
    # required = lambda x: not x in load
    # parser.add_argument("-a", "--auth_service", help="Auth Service ('ptc' or 'google')",
    #     required=required("auth_service"))
    # parser.add_argument("-u", "--username", help="Username", required=required("username"))
    # parser.add_argument("-p", "--password", help="Password", required=required("password"))
    # parser.add_argument("-l", "--location", help="Location", required=required("location"))
    # parser.add_argument("-d", "--debug", help="Debug Mode", action='store_true')
    # parser.add_argument("-t", "--test", help="Only parse the specified location", action='store_true')
    # parser.set_defaults(DEBUG=False, TEST=False)
    # config = parser.parse_args()

    # # Passed in arguments shoud trump
    # for key in config.__dict__:
    #     if key in load and config.__dict__[key] == None:
    #         config.__dict__[key] = load[key]

    # if config.auth_service not in ['ptc', 'google']:
    #   log.error("Invalid Auth service specified! ('ptc' or 'google')")
    #   return None
    # return config


# def main():

#     MOST_WANTED_POKEMON_ID = [16, 133]
#     #client = pykemon.V1Client()
#     # log settings
#     # log format
#     logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(module)10s] [%(levelname)5s] %(message)s')
#     # log level for http request class
#     logging.getLogger("requests").setLevel(logging.WARNING)
#     # log level for main pgoapi class
#     logging.getLogger("pgoapi").setLevel(logging.INFO)
#     # log level for internal pgoapi class
#     logging.getLogger("rpc_api").setLevel(logging.INFO)

#     config = init_config()
#     if not config:
#         return

#     if config.debug:
#         logging.getLogger("requests").setLevel(logging.DEBUG)
#         logging.getLogger("pgoapi").setLevel(logging.DEBUG)
#         logging.getLogger("rpc_api").setLevel(logging.DEBUG)

#     position = get_pos_by_name(config.location)
#     print position
#     if config.test:
#         return

#     # instantiate pgoapi
#     api = PGoApi()

#     # provide player position on the earth
#     api.set_position(*position)

#     if not api.login(config.auth_service, config.username, config.password):
#         return

#     # chain subrequests (methods) into one RPC call
#     # get player profile call
#     #api.get_player()

#     # get inventory call
#     #api.get_inventory()

#     # get map objects call
#     timestamp = "\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"
#     cellid = get_cellid(position[0], position[1])
#     api.get_map_objects(latitude=f2i(position[0]), longitude=f2i(position[1]), since_timestamp_ms=timestamp, cell_id=cellid)

#     # get download settings call
#     #api.download_settings(hash="4a2e9bc330dae60e7b74fc85b98868ab4700802e")

#     # execute the RPC call
#     response_dict = api.call()
#     map_cells = response_dict['responses']['GET_MAP_OBJECTS']['map_cells']
#     for cell in map_cells:
#         # if "nearby_pokemons" in cell:
#         #     print "nearby_pokemons"
#         #     print cell['nearby_pokemons']
#         if "catchable_pokemons" in cell:
#             #print "catchable_pokemons"
#             print cell['catchable_pokemons']
#             for pokemon in cell['catchable_pokemons']:
#                 pokemon_id = int(pokemon['pokemon_id'])
#                 longitude = float(pokemon['longitude'])
#                 latitude = float(pokemon['latitude'])
#                 expiration_timestamp_ms = pokemon['expiration_timestamp_ms']
#                 if pokemon_id in MOST_WANTED_POKEMON_ID:
#                     print "pokemon_id",pokemon_id
#                     print longitude
#                     print latitude
#                 #no1 = Pokemon(pid=pokemon_id,lat=latitude,lng=longitude, report_time =  datetime.now() )
#                 #no1.save()
#                     #print expiration_timestamp_ms
#                 #print pokemon_id
#                 #p = client.get_pokemon(uid=pokemon_id)
#                 #print p['name']

#     #print response_dict['responses']['GET_MAP_OBJECTS']['map_cells']
#     #print len(response_dict['responses']['GET_MAP_OBJECTS']['map_cells'])

#     #print('Response dictionary: \n\r{}'.format(json.dumps(response_dict, indent=2)))
# #json.JSONEncoder().encode({"foo": ["bar", "baz"]})
# #'{"foo": ["bar", "baz"]}'
#     # alternative:
#     # api.get_player().get_inventory().get_map_objects().download_settings(hash="4a2e9bc330dae60e7b74fc85b98868ab4700802e").call()


def main_2(position):
    MOST_WANTED_POKEMON_ID = [16, 133]
    #client = pykemon.V1Client()
    # log settings
    # log format
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(module)10s] [%(levelname)5s] %(message)s')
    # log level for http request class
    logging.getLogger("requests").setLevel(logging.WARNING)
    # log level for main pgoapi class
    logging.getLogger("pgoapi").setLevel(logging.INFO)
    # log level for internal pgoapi class
    logging.getLogger("rpc_api").setLevel(logging.INFO)

    config = init_config()
    if not config:
        return

    if config.debug:
        logging.getLogger("requests").setLevel(logging.DEBUG)
        logging.getLogger("pgoapi").setLevel(logging.DEBUG)
        logging.getLogger("rpc_api").setLevel(logging.DEBUG)

    #position = get_pos_by_name(config.location)
    #print position
    if config.test:
        return

    start_lat = position[0]
    start_lon = position[1]

    position = (start_lat, start_lon, 0.0) 
    api = PGoApi()

    #main_2(loc)
    # provide player position on the earth
    api.set_position(*position)

    if not api.login(config.auth_service, config.username, config.password):
        return

    # chain subrequests (methods) into one RPC call
    # get player profile call
    #api.get_player()

    # get inventory call
    #api.get_inventory()

    # get map objects call
    timestamp = "\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"
    cellid = get_cellid(position[0], position[1])
    try:
        ENCOUNTER_ID_LIST  = load_data('./ENCOUNTER_ID_LIST.data')
    except:
        ENCOUNTER_ID_LIST = []
    ENCOUNTER_ID_LIST = collections.deque(ENCOUNTER_ID_LIST)
    for i in xrange(16):
        next_lat, next_lon = move(start_lat, start_lon, 0.01, 30)
        #print next_lat, next_lon
        position = (next_lat, next_lon, 0.0)
        api.set_position(*position)

        api.get_map_objects(latitude=f2i(position[0]), longitude=f2i(position[1]), since_timestamp_ms=timestamp, cell_id=cellid)

        # get download settings call
        #api.download_settings(hash="4a2e9bc330dae60e7b74fc85b98868ab4700802e")

        # execute the RPC call
        try:
            response_dict = api.call()
            map_cells = response_dict['responses']['GET_MAP_OBJECTS']['map_cells']
            for cell in map_cells:
                # if "nearby_pokemons" in cell:
                #     print "nearby_pokemons"
                #     print cell['nearby_pokemons']
                if "catchable_pokemons" in cell:
                    #print "catchable_pokemons"
                    print cell['catchable_pokemons']
                    for pokemon in cell['catchable_pokemons']:
                        pokemon_id = int(pokemon['pokemon_id'])
                        longitude = float(pokemon['longitude'])
                        latitude = float(pokemon['latitude'])
                        encounter_id = str(pokemon['encounter_id'])
                        expiration_timestamp_ms = str(pokemon['expiration_timestamp_ms'])
                        if encounter_id not in ENCOUNTER_ID_LIST:
                            print "pokemon_id: ",pokemon_id
                            print longitude
                            print latitude
                            new_pokemon = Pokemon(pid=pokemon_id,lat=latitude,lng=longitude, encounter_id= encounter_id, report_time = datetime.now() )
                            new_pokemon.save()
                            ENCOUNTER_ID_LIST.append(encounter_id)
                            if len(ENCOUNTER_ID_LIST) > 5000:
                                ENCOUNTER_ID_LIST.popleft()

            start_lat, start_lon = next_lat, next_lon
            sleep(10)
        except Exception, e:
            print e
            pass
    save_data(ENCOUNTER_ID_LIST)

def save_data(dataset):
    outputFile = 'ENCOUNTER_ID_LIST.data'
    fw = open(outputFile, 'w')
    pickle.dump(dataset, fw)
    fw.close()

def load_data(filename):
    fr = open(filename)
    dataset = pickle.load(fr)
    return dataset

def move(lat1, lon1, d=0.01, b=0):
    # lat1 = 43.0863282
    # lon1 = -79.0690467
    # b = 90 #Bearing is 90 degrees converted to radians.
    # d = 0.005 #Distance in km
    origin = geopy.Point(lat1, lon1)
    destination = VincentyDistance(kilometers=d).destination(origin, b)
    lat2, lon2 = destination.latitude, destination.longitude
    return lat2,lon2

if __name__ == '__main__':
    #main()
    try:
        while 1:
            main_2([43.0007, -78.782873])
    except:
        print "ERROR!!!!!!!!!!!!!!!"

    # for i in xrange(1):
    #     next_lat, next_lon = move(start_lat, start_lon)
    #     print next_lat, next_lon
    #     loc = (next_lat, next_lon, 0.0)
    #     main_2(loc)
    #     start_lat, start_lon = next_lat, next_lon
    #     sleep(5)
    #
