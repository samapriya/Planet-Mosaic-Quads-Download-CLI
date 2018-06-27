#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import os
import csv
import ee
from planet.api.utils import read_planet_json
from planet.api.auth import find_api_key
ee.Initialize()
os.chdir(os.path.dirname(os.path.realpath(__file__)))
pathway=os.path.dirname(os.path.realpath(__file__))
try:
    PL_API_KEY = find_api_key()
    os.environ['PLANET_API_KEY']=find_api_key()
except:
    print('Failed to get Planet Key: Initialize First')
    sys.exit()

SESSION = requests.Session()
SESSION.auth = (PL_API_KEY, '')
with open(os.path.join(pathway,"ids.csv"),'wb') as csvfile:
        writer=csv.DictWriter(csvfile,fieldnames=["id","minx","miny","maxx","maxy"], delimiter=',')
        writer.writeheader()
def handle_page(page,year,minx,miny,maxx,maxy):
    n=0
    for items in page['mosaics']:
        if items['name'].startswith('global_monthly_'+str(year)):
            #print(items['name'],items['id'])
            with open(os.path.join(pathway,"ids.csv"),'a') as csvfile:
                writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                writer.writerow([items['id'],minx,miny,maxx,maxy])
def idl(infile,start,end):
    headers = {'Content-Type': 'application/json'}
    PL_API_KEY = read_planet_json()['key']
    for year in range(int(start),int(end)+1):
        cdx=[]
        cdy=[]
        with open(infile) as aoi:
            geomloader = json.load(aoi)
            cinsert= geomloader['features'][0]['geometry']['coordinates']
            cin=ee.Geometry.Polygon(cinsert).bounds().getInfo()['coordinates'][0]
            for coord in str(cin).split('],'):
                x=(coord.replace('[','').replace(']','').split(',')[0].strip())
                y=(coord.replace('[','').replace(']','').split(',')[1].strip())
                cdx.append(x)
                cdy.append(y)
            maxx=(max(cdx))
            minx=(min(cdx))
            maxy=(max(cdy))
            miny=(min(cdy))
            #print(maxx,minx,maxy,miny)
        ## Send get request
            result = requests.get('https://api.planet.com/mosaic/experimental/mosaics',auth=(PL_API_KEY, ''))
            page=result.json()
            final_list = handle_page(page,year,minx,miny,maxx,maxy)
            while page['_links'].get('_next') is not None:
                page_url = page['_links'].get('_next')
                page = SESSION.get(page_url).json()
                ids = handle_page(page,year,minx,miny,maxx,maxy)
#idl(infile=os.path.join(r'C:\planet_demo\mapbiomas','SH_22_Y_D.geojson'),year="2018")

