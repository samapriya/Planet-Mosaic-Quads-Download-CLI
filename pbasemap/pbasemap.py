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
import os
import argparse
import csv
import sys
from geom_rbox import idl
from mos_download import download
from mos_pydl import pydownload
from shp2geojson import shp2gj
from mosaic_metadata import metadata
os.chdir(os.path.dirname(os.path.realpath(__file__)))
pathway = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pathway)


def mosaic_list_from_parser(args):
    idl(infile=args.geometry,start=args.start, end=args.end)

def download_mosaic_from_parser(args):
    download(ids=args.id, infile=args.geometry,coverage=args.coverage,local=args.local)

def multipart_mosaic_from_parser(args):
    pydownload(ids=args.id, infile=args.geometry,coverage=args.coverage,local=args.local)

def metadata_from_parser(args):
    metadata(infile=args.geometry, start=args.start,end=args.end,outfile=args.output)

def shp2gj_metadata_from_parser(args):
    shp2gj(folder=args.source, export=args.destination)



def main(args=None):
    parser = \
        argparse.ArgumentParser(description='Planet Mosaic Quads Download CLI'
                                )

    subparsers = parser.add_subparsers()

    parser_idl = subparsers.add_parser('mosaic_list',
            help='Tool to get Mosaic & Bounding Box list')
    parser_idl.add_argument('--geometry',
                            help='Choose a geometry file supports GeoJSON, KML')
    parser_idl.add_argument('--start', help='Choose Start date in format YYYY-MM-DD')
    parser_idl.add_argument('--end', help='Choose End date in format YYYY-MM-DD')
    parser_idl.set_defaults(func=mosaic_list_from_parser)

    parser_download = subparsers.add_parser('download',help='Download quad GeoTiffs')
    parser_download.add_argument('--id', help='Mosaic ID from earlier search')
    parser_download.add_argument('--geometry',
                            help='Choose a geometry file supports GeoJSON, KML')
    parser_download.add_argument('--local', help='Local folder to download images')
    optional_named = parser_download.add_argument_group('Optional named arguments')
    optional_named.add_argument('--coverage', help="Choose minimum percentage coverage", default=None)
    parser_download.set_defaults(func=download_mosaic_from_parser)

    parser_multipart_mosaic = subparsers.add_parser('mpdownload',help='Download quad GeoTiffs using multipart downloader')
    parser_multipart_mosaic.add_argument('--id', help='Mosaic ID from earlier search')
    parser_multipart_mosaic.add_argument('--geometry',
                            help='Choose a geometry file supports GeoJSON, KML')
    parser_multipart_mosaic.add_argument('--local', help='Local folder to download images')
    optional_named = parser_multipart_mosaic.add_argument_group('Optional named arguments')
    optional_named.add_argument('--coverage', help="Choose minimum percentage coverage", default=None)
    parser_multipart_mosaic.set_defaults(func=multipart_mosaic_from_parser)

    parser_metadata = subparsers.add_parser('metadata',help='Download Quad Metadata')
    parser_metadata.add_argument('--geometry',help='Choose a geometry file supports GeoJSON, KML')
    parser_metadata.add_argument('--start', help='Choose Start date in format YYYY-MM-DD')
    parser_metadata.add_argument('--end', help='Choose End date in format YYYY-MM-DD')
    parser_metadata.add_argument('--output', help='Full path where you want the metadata exported')
    parser_metadata.set_defaults(func=metadata_from_parser)

    parser_shp2gj = subparsers.add_parser('shp2geojson',help='Convert all shapefiles in folder to GeoJSON')
    parser_shp2gj.add_argument('--source', help='Choose Source Folder')
    parser_shp2gj.add_argument('--destination', help='Choose Destination Folder')
    parser_shp2gj.set_defaults(func=shp2gj_metadata_from_parser)
    args = parser.parse_args()

    args.func(args)


if __name__ == '__main__':
    main()



