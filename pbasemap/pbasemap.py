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
from mos_pydl import multipart
from shp2geojson import shp2gj
from mosaic_metadata import metadata
os.chdir(os.path.dirname(os.path.realpath(__file__)))
pathway = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pathway)


def rbox_from_parser(args):
    idl(infile=args.geometry)


def mosaic_list_from_parser(args):
    metadata(infile=args.geometry, start=args.start,end=args.end,outfile=args.output)


def download_mosaic_from_parser(args):
    download(names=args.name, ids=None, idlist=args.idlist,infile=args.geometry,coverage=args.coverage,local=args.local)

def multipart_mosaic_from_parser(args):
    multipart(names=args.name, ids=None, idlist=args.idlist,infile=args.geometry,coverage=args.coverage,local=args.local)


def shp2gj_metadata_from_parser(args):
    shp2gj(folder=args.source, export=args.destination)



def main(args=None):
    parser = \
        argparse.ArgumentParser(description='Planet Mosaic Quads Download CLI'
                                )

    subparsers = parser.add_subparsers()

    parser_rbox = subparsers.add_parser('rbox',
            help='Prints bounding box for geometry')
    parser_rbox.add_argument('--geometry',
                            help='Choose a geometry file supports GeoJSON, KML')
    parser_rbox.set_defaults(func=rbox_from_parser)

    parser_mosaic_list = subparsers.add_parser('mosaic_list',
            help='Tool to get Mosaic & Bounding Box list')
    parser_mosaic_list.add_argument('--geometry',
                            help='Choose a geometry file supports GeoJSON, KML')
    parser_mosaic_list.add_argument('--start', help='Choose Start date in format YYYY-MM-DD')
    parser_mosaic_list.add_argument('--end', help='Choose End date in format YYYY-MM-DD')
    parser_mosaic_list.add_argument('--output', help='Full path where you want your mosaic list exported')
    parser_mosaic_list.set_defaults(func=mosaic_list_from_parser)

    parser_download = subparsers.add_parser('download',help='Download quad GeoTiffs choose from name or idlist')
    parser_download.add_argument('--geometry',
                            help='Choose a geometry file supports GeoJSON, KML')
    parser_download.add_argument('--local', help='Local folder to download images')
    optional_named = parser_download.add_argument_group('Optional named arguments')
    optional_named.add_argument('--coverage', help="Choose minimum percentage coverage", default=None)
    optional_named.add_argument('--name', help='Mosaic name from earlier search or csvfile', default=None)
    optional_named.add_argument('--idlist', help="Mosaic list csvfile", default=None)
    parser_download.set_defaults(func=download_mosaic_from_parser)

    parser_multipart_mosaic = subparsers.add_parser('mpdownload',help='Download quad GeoTiffs using multipart downloader')
    parser_multipart_mosaic.add_argument('--geometry',
                            help='Choose a geometry file supports GeoJSON, KML')
    parser_multipart_mosaic.add_argument('--local', help='Local folder to download images')
    optional_named = parser_multipart_mosaic.add_argument_group('Optional named arguments')
    optional_named.add_argument('--coverage', help="Choose minimum percentage coverage", default=None)
    optional_named.add_argument('--name', help='Mosaic name from earlier search or csvfile', default=None)
    optional_named.add_argument('--idlist', help="Mosaic list csvfile", default=None)
    parser_multipart_mosaic.set_defaults(func=multipart_mosaic_from_parser)

    parser_shp2gj = subparsers.add_parser('shp2geojson',help='Convert all shapefiles in folder to GeoJSON')
    parser_shp2gj.add_argument('--source', help='Choose Source Folder')
    parser_shp2gj.add_argument('--destination', help='Choose Destination Folder')
    parser_shp2gj.set_defaults(func=shp2gj_metadata_from_parser)
    args = parser.parse_args()

    args.func(args)


if __name__ == '__main__':
    main()



