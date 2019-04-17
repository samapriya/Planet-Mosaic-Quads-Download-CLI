__copyright__ = """

    Copyright 2019 Samapriya Roy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""
__license__ = "Apache 2.0"

#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import csv
import sys
import pyproj
from datetimerange import DateTimeRange
from functools import partial
from shapely.geometry import shape
from shapely.geometry import Polygon
from shapely.ops import transform
from shapely.geometry import box
from planet.api.auth import find_api_key

#Create an empty geojson template
temp={"coordinates":[],"type":"Polygon"}
try:
    PL_API_KEY = find_api_key()
except:
    print('Failed to get Planet Key')
    sys.exit()
SESSION = requests.Session()
SESSION.auth = (PL_API_KEY, '')

def handle_page(response, gmainbound,start, end,outfile):
    for items in response['mosaics']:
        bd = items['bbox']
        mosgeom = shape(Polygon(box(bd[0], bd[1], bd[2], bd[3]).exterior.coords))
        gboundlist = gmainbound.split(',')
        boundgeom = shape(Polygon(box(float(gboundlist[0]), float(gboundlist[1]), float(gboundlist[2]), float(gboundlist[3]))))
        proj = partial(pyproj.transform, pyproj.Proj(init='epsg:4326'), pyproj.Proj(init='epsg:3857'))
        boundgeom = transform(proj, boundgeom)
        mosgeom = transform(proj, mosgeom)
        if boundgeom.intersection(mosgeom).is_empty:
            pass
        else:
            id = items['id']
            r = requests.get('https://api.planet.com/mosaic/experimental/mosaics/' + str(id) + '/quads?bbox=' + str(gboundlist[0])+'%2C'+gboundlist[1]+'%2C'+gboundlist[2]+'%2C'+gboundlist[3],auth=(PL_API_KEY,''))
            resp = r.json()
            if len(resp['items']) > 0:
                time_range = DateTimeRange(items['first_acquired'].split('T')[0], items['last_acquired'].split('T')[0])
                x = DateTimeRange(start, end)
                if time_range.is_intersection(x) is True:
                    #print(boundgeom.intersection(mosgeom).area/1000000)
                    print('Mosaic name:  ' + str(items['name']))
                    print('Mosaic Resolution:  ' + str(items['grid']['resolution']))
                    print('Mosaic ID:  ' + str(items['id']))
                    name=str(items['name'])
                    ids=str(items['id'])
                    facq=str(items['first_acquired']).split('T')[0]
                    lacq=str(items['last_acquired']).split('T')[0]
                    res=str(items['grid']['resolution'])
                    print('')
                    with open(outfile,'a') as csvfile:
                        writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                        writer.writerow([name, ids, facq,lacq,format(float(res),'.3f')])
                    csvfile.close()


def metadata(infile,start,end,outfile):
    headers = {'Content-Type': 'application/json'}

    with open(outfile,'w') as csvfile:
        writer=csv.DictWriter(csvfile,fieldnames=["name", "id", "first_acquired",
                                                  "last_acquired","resolution"], delimiter=',')
        writer.writeheader()
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
    print('rbox:' + str(gmainbound)+'\n')
    r = requests.get('https://api.planet.com/basemaps/v1/mosaics', auth=(PL_API_KEY, ''))
    response = r.json()
    final_list = handle_page(response, gmainbound, start, end,outfile)
    try:
        while response['_links'].get('_next') is not None:
            page_url = response['_links'].get('_next')
            r = requests.get(page_url)
            response = r.json()
            idlist = handle_page(response, gmainbound, start, end,outfile)
    except Exception as e:
        print(e)
    except (KeyboardInterrupt, SystemExit) as e:
        print('Program escaped by User')
        sys.exit()
    print('rbox:' + str(gmainbound))
# metadata(infile=r'C:\Users\samapriya\Downloads\belem.geojson',start='2018-10-02',end='2019-03-01',outfile=r'C:\planet_demo\mosmeta.csv')
