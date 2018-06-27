import os,argparse,csv
from mosaic_grid import idl
from download_mosaic import download
from mosaic_metadata import idm
from shp2geojson import shp2gj
from planet.api.auth import find_api_key
os.chdir(os.path.dirname(os.path.realpath(__file__)))
pathway=os.path.dirname(os.path.realpath(__file__))
def mosaic_list_from_parser(args):
    with open(os.path.join(pathway,"ids.csv"),'wb') as csvfile:
        writer=csv.DictWriter(csvfile,fieldnames=["id","minx","miny","maxx","maxy"], delimiter=',')
        writer.writeheader()
    for filelist in os.listdir(args.local):
        if filelist.endswith('.geojson'):
            print('')
            print('Processing Grid '+str(filelist))
            idl(infile=os.path.join(args.local,filelist),start=args.start,end=args.end)
def download_mosaic_from_parser(args):
    download(filepath=args.local,coverage=args.coverage)
def download_metadata_from_parser(args):
    idm(start=args.start,end=args.end)
def shp2gj_metadata_from_parser(args):
    shp2gj(folder=args.source,export=args.destination)
    
def main(args=None):
    parser = argparse.ArgumentParser(description='Planet Mosaic Quads Download CLI')

    subparsers = parser.add_subparsers()

    parser_idl=subparsers.add_parser('mosaic_list',help='Tool to get Mosaic & Bounding Box list')
    parser_idl.add_argument('--local', help='Choose folder with geojson files')
    parser_idl.add_argument('--start', help='Choose Start Year')
    parser_idl.add_argument('--end', help='Choose End Year')
    parser_idl.set_defaults(func=mosaic_list_from_parser)

    parser_download=subparsers.add_parser('download_quad',help='Download metadata quads')
    parser_download.add_argument('--local', help='Choose folder with geojson files')
    parser_download.add_argument('--coverage', help='Choose folder with geojson files')
    parser_download.set_defaults(func=download_mosaic_from_parser)

    parser_idm=subparsers.add_parser('download_metadata',help='Download Quad Metadata')
    parser_idm.add_argument('--start', help='Choose Start Year')
    parser_idm.add_argument('--end', help='Choose End Year')
    parser_idm.set_defaults(func=download_metadata_from_parser)

    parser_shp2gj=subparsers.add_parser('shp2geojson',help='Convert all shapefiles in folder to GeoJSON')
    parser_shp2gj.add_argument('--source', help='Choose Source Folder')
    parser_shp2gj.add_argument('--destination', help='Choose Destination Folder')
    parser_shp2gj.set_defaults(func=shp2gj_metadata_from_parser)
    args = parser.parse_args()

    args.func(args)

if __name__ == '__main__':
    main()

