import requests,json,re,csv,os,subprocess,urllib2,getpass,sys
from pprint import pprint
from os.path import expanduser
from urllib2 import Request, urlopen
from os.path import expanduser
from retrying import retry
from planet.api.utils import read_planet_json
from planet.api.auth import find_api_key
os.chdir(os.path.dirname(os.path.realpath(__file__)))
planethome=os.path.dirname(os.path.realpath(__file__))
try:
    PL_API_KEY = find_api_key()
    os.environ['PLANET_API_KEY']=find_api_key()
except:
    print('Failed to get Planet Key: Initialize First')
    sys.exit()
CAS_URL='https://api.planet.com/mosaic/experimental/mosaics'
headers = {'Content-Type': 'application/json',}
def download(filepath=None):
        with open(os.path.join(planethome,"ids.csv")) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                        url=('https://api.planet.com/mosaic/experimental/mosaics/'+str(row['id'])+'/quads?bbox='+str(row['maxx'])+'%2C'+str(row['maxy'])+'%2C'+str(row['minx'])+'%2C'+str(row['miny']))
                        main=requests.get(url,auth=(PL_API_KEY, '')).json()
                        for stuff in main['items']:
                                downlink='https://api.planet.com/mosaic/experimental/mosaics/'+row['id']+'/quads/'+stuff['id']+'/full?api_key='+str(PL_API_KEY)
                                #print(downlink)
                                r = requests.get(downlink, allow_redirects=False, timeout=0.5)
                                mos=(r.headers['location'].split('planet-mosaics-prod/')[1].split('/')[0])
                                fn=(r.headers['location'].split('%')[-2])
                                filename=mos+'_'+fn
                                filelink = urllib2.urlopen(downlink)
                                ov=os.path.join(filepath,filename)
                                if not os.path.exists(ov):
                                    try:
                                            print("Downloading: "+str(filename))
                                            with open(ov, "wb") as code:
                                                code.write(filelink.read())
                                            
                                    except Exception as e:
                                            print(e)
                                else:
                                    print("asset exists..Skipping "+str(filename))
