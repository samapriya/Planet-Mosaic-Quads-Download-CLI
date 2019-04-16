#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import os
import sys
from shapely.geometry import shape
from planet.api.auth import find_api_key
os.chdir(os.path.dirname(os.path.realpath(__file__)))
planethome = os.path.dirname(os.path.realpath(__file__))


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
def download(ids, infile,coverage,local):
    headers = {'Content-Type': 'application/json'}

##Parse Geometry
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
                    r = requests.get(downlink,allow_redirects=False, timeout=0.5)
                    filelink=r.headers['Location']
                    filename=str(r.headers['Location']).split('%22')[-2]
                    localpath=os.path.join(local,filename)
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
                elif coverage is None:
                    downlink = itemlist['_links']['download']
                    r = requests.get(downlink,allow_redirects=False, timeout=0.5)
                    filelink=r.headers['Location']
                    filename=str(r.headers['Location']).split('%22')[-2]
                    localpath=os.path.join(local,filename)
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

##download(ids='af953970-7189-473a-8e26-24397577eaa2',infile=r'C:\Users\samapriya\Downloads\belem.geojson',coverage=80,
##    local=r'C:\planet_demo')
            # except Exception as e:
            #     print(e)

