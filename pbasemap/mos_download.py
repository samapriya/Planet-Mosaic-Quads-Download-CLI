#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import os
import sys
import csv
from shapely.geometry import shape
from planet.api.auth import find_api_key
os.chdir(os.path.dirname(os.path.realpath(__file__)))
planethome = os.path.dirname(os.path.realpath(__file__))

idmatch=[]

# Create an empty geojson template
temp = {"coordinates":[], "type":"Polygon"}
try:
    PL_API_KEY = find_api_key()
    os.environ['PLANET_API_KEY'] = find_api_key()
except:
    print('Failed to get Planet Key: Initialize First')
    sys.exit()
SESSION = requests.Session()
SESSION.auth = (PL_API_KEY, '')
CAS_URL = 'https://api.planet.com/mosaic/experimental/mosaics/'


# Function to download the geotiffs
def download(ids,names, idlist, infile, coverage, local):
    if idlist is None and names is not None:
        downloader(ids,names, infile, coverage, local)
    elif idlist is not None:
        with open(idlist) as csvfile:
            reader=csv.DictReader(csvfile)
            for row in reader:
                print('')
                print('Processing: '+str(row['name']))
                downloader(str(row['id']),str(row['name']),infile, coverage, local)

# Get item id from item name
def handle_page(names,response):
    for items in response['mosaics']:
        if items['name']==names:
            return items['id']

# Downloader
def downloader(ids,names, infile, coverage, local):
    if names is None and ids is not None:
        ids=ids
    elif names is not None and ids is None:
        resp=SESSION.get('https://api.planet.com/basemaps/v1/mosaics')
        response=resp.json()
        ids=handle_page(names,response)
        idmatch.append(ids)
        try:
            while response['_links'].get('_next') is not None:
                page_url = response['_links'].get('_next')
                r = requests.get(page_url)
                response = r.json()
                ids = handle_page(names,response)
                idmatch.append(ids)
        except Exception as e:
            print(e)
        for ival in idmatch:
            if ival is not None:
                ids=ival
    elif names is not None and ids is not None:
        ids = ids
    headers = {'Content-Type': 'application/json'}
    try:
        if infile.endswith('.geojson'):
            with open(infile) as aoi:
                aoi_resp = json.load(aoi)
                aoi_geom = aoi_resp['features'][0]['geometry']['coordinates']
        elif infile.endswith('.json'):
            with open (infile) as aoi:
                aoi_resp=json.load(aoi)
                aoi_geom=aoi_resp['config'][0]['config']['coordinates']
        elif infile.endswith('.kml'):
            getcoord=kml2coord(infile)
            aoi_geom=getcoord
    except Exception as e:
        print('Could not parse geometry')
        print(e)

    temp['coordinates'] = aoi_geom
    gmain = shape(temp)
    gmainbound = (','.join(str(v) for v in list(gmain.bounds)))
    gboundlist = gmainbound.split(',')
    url = CAS_URL \
        + str(ids) + '/quads?bbox=' + str(gboundlist[0]) \
        + '%2C' + str(gboundlist[1]) + '%2C' + str(gboundlist[2]) \
        + '%2C' + str(gboundlist[3])
    main = SESSION.get(url)
    try:
        if main.status_code == 200:
            resp = main.json()
            for itemlist in resp['items']:
                if coverage is not None and int(itemlist['percent_covered']) >= int(coverage):
                    downlink = itemlist['_links']['download']
                    r = requests.get(downlink,allow_redirects=False)
                    filelink = r.headers['Location']
                    filename = str(r.headers['Location']).split('%22')[-2]
                    localpath = os.path.join(local, names+'_'+filename)
                    result = SESSION.get(filelink)
                    if not os.path.exists(localpath) and result.status_code == 200:
                        print("Downloading: " + str(localpath))
                        f = open(localpath, 'wb')
                        for chunk in result.iter_content(chunk_size=512 * 1024):
                            if chunk:
                                f.write(chunk)
                        f.close()
                    else:
                        if int(result.status_code) != 200:
                            print("Encountered error with code: " + str(result.status_code) + ' for ' + str(localpath))
                        elif int(result.status_code) == 200:
                            print("File already exists SKIPPING: " + str(localpath))
                elif coverage is None:
                    downlink = itemlist['_links']['download']
                    r = requests.get(downlink,allow_redirects=False)
                    filelink=r.headers['Location']
                    filename=str(r.headers['Location']).split('%22')[-2]
                    localpath=os.path.join(local,names+'_'+filename)
                    #print(filename)
                    result = SESSION.get(filelink)
                    if not os.path.exists(localpath) and result.status_code == 200:
                        print("Downloading: " + str(localpath))
                        f = open(localpath, 'wb')
                        for chunk in result.iter_content(chunk_size=512 * 1024):
                            if chunk:
                                f.write(chunk)
                        f.close()
                    else:
                        if int(result.status_code) != 200:
                            print("Encountered error with code: " + str(result.status_code) + ' for ' + str(localpath))
                        elif int(result.status_code) == 200:
                            print("File already exists SKIPPING: " + str(localpath))
    except Exception as e:
        print(e)
    except (KeyboardInterrupt, SystemExit) as e:
        print('Program escaped by User')
        sys.exit()

# download(names=None,ids=None,idlist=r'C:\planet_demo\moslist.csv',infile=r'C:\Users\samapriya\Downloads\belem.geojson',coverage=80,
#    local=r'C:\planet_demo')

