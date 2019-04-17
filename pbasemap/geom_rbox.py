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

import json
import sys
from shapely.geometry import shape
from shapely.geometry import box

#Create an empty geojson template
temp={"coordinates":[],"type":"Polygon"}

def idl(infile):
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
    except (KeyboardInterrupt, SystemExit) as e:
        print('Program escaped by User')
        sys.exit()
    temp['coordinates'] = aoi_geom
    gmain = shape(temp)
    gmainbound = (','.join(str(v) for v in list(gmain.bounds)))
    print('')
    print('rbox:')
    print(str(gmainbound))
#idl(infile=r'C:\Users\samapriya\Downloads\belem.geojson')
