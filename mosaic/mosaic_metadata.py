#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import os
import csv
import time
from planet.api.utils import read_planet_json
from planet.api.auth import find_api_key
os.chdir(os.path.dirname(os.path.realpath(__file__)))
pathway = os.path.dirname(os.path.realpath(__file__))
try:
    PL_API_KEY = find_api_key()
    os.environ['PLANET_API_KEY'] = find_api_key()
except:
    print 'Failed to get Planet Key: Initialize First'
    sys.exit()
SESSION = requests.Session()
SESSION.auth = (PL_API_KEY, '')
with open(os.path.join(pathway, 'idmetadata.csv'), 'wb') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=[
        'name',
        'coordinate_system',
        'id',
        'first_acquired',
        'last_acquired',
        'quad_size',
        'resolution',
        'level',
        ], delimiter=',')
    writer.writeheader()


def handle_page(page, year):
    n = 0
    for items in page['mosaics']:
        if items['name'].startswith('global_monthly_' + str(year)):
            name = items['name']
            coordinate_system = items['coordinate_system']
            ids = items['id']
            first_acquired = items['first_acquired']
            last_acquired = items['last_acquired']
            quad_size = items['grid']['quad_size']
            resolution = items['grid']['resolution']
            level = items['level']
            print name
            date_time = first_acquired.split('T')[0]
            pattern = '%Y-%m-%d'
            epoch_first = int(time.mktime(time.strptime(date_time,
                              pattern))) * 1000
            date_time = last_acquired.split('T')[0]
            pattern = '%Y-%m-%d'
            epoch_last = int(time.mktime(time.strptime(date_time,
                             pattern))) * 1000
            with open(os.path.join(pathway, 'idmetadata.csv'), 'a') as \
                csvfile:
                writer = csv.writer(csvfile, delimiter=',',
                                    lineterminator='\n')
                writer.writerow([
                    name,
                    coordinate_system,
                    ids,
                    epoch_first,
                    epoch_last,
                    quad_size,
                    resolution,
                    level,
                    ])

def idm(start, end):
    headers = {'Content-Type': 'application/json'}
    PL_API_KEY = read_planet_json()['key']
    for year in range(int(start), int(end) + 1):
        result = \
            requests.get('https://api.planet.com/mosaic/experimental/mosaics'
                         , auth=(PL_API_KEY, ''))
        page = result.json()
        final_list = handle_page(page, year)
        while page['_links'].get('_next') is not None:
            page_url = page['_links'].get('_next')
            page = SESSION.get(page_url).json()
            ids = handle_page(page, year)


# idm(start=2016,end=2018)
