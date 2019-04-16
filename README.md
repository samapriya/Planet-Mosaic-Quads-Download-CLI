# Planet-Mosaic-Quads-Download-CLI
[![PyPI version](https://badge.fury.io/py/pbasemap.svg)](https://badge.fury.io/py/pbasemap)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1432872.svg)](https://doi.org/10.5281/zenodo.1432872)

Planet creates global monthly mosaics apart from creating mosaics at different frequencies, monthly mosaics are of interest to a lot of people who would like to do a consistent time series analysis using these mosaics and would like to apply them to an existing analytical pipeline. I created this tool to allow you pass single or multiple geometries in a folder for the tool to find the mosaic quads and then process and download it. For now the geometry is passed as a geojson file, but I have included a tool for you to convert any shapefile into geojson files so you can use this tool. In the future I will add support for kml and json files as well.

## Table of contents
* [Installation](#installation)
* [Getting started](#getting-started)
* [pbasemap Planet Mosaic Quads Download CLI](#pbasemap-planet-mosaic-quads-download-cli)
    * [mosaic list](#mosaic-list)
    * [download mosaic](#download-mosaic)
    * [download mosaic metadata](#download-mosaic-metadata)
    * [multipart download mosaic](#multipart-download-mosaic)
    * [shape to geojson](#shape-to-geojson)

## Installation
This assumes that you have native python & pip installed in your system, you can test this by going to the terminal (or windows command prompt) and trying

```python``` and then ```pip list```

If you get no errors and you have python 2.7.14 or higher you should be good to go. Please note that I have tested this only on python 2.7.15 but it should run on python 3.

To install **pbasemap: Planet Mosaic Quads Download CLI** you can install using two methods

```pip install pbasemap```

or you can also try

```
git clone https://github.com/samapriya/Planet-Mosaic-Quads-Download-CLI.git
cd pbasemap
python setup.py install
```
For **linux use sudo and for windows right click the command prompt and run as admin**.

Installation is an optional step; the application can be also run directly by executing pbasemap.py script. The advantage of having it installed is being able to execute ppipe as any command line tool. I recommend installation within virtual environment. If you don't want to install, browse into the pbasemap folder and try ```python pbasemap.py``` to get to the same result.


## Getting started

As usual, to print help:

```
usage: pbasemap [-h]
                {mosaic_list,download,mpdownload,metadata,shp2geojson} ...

Planet Mosaic Quads Download CLI

positional arguments:
  {mosaic_list,download,mpdownload,metadata,shp2geojson}
    mosaic_list         Tool to get Mosaic & Bounding Box list
    download            Download quad GeoTiffs
    mpdownload          Download quad GeoTiffs using multipart downloader
    metadata            Download Quad Metadata
    shp2geojson         Convert all shapefiles in folder to GeoJSON

optional arguments:
  -h, --help            show this help message and exit
  ```

To obtain help for a specific functionality, simply call it with _help_ switch, e.g.: `pbasemap zipshape -h`. If you didn't install pbasemap, then you can run it just by going to *pbasemap* directory and running `python pbasemap.py [arguments go here]`

## pbasemap Simple CLI for Basemaps API
The tool allows you to list and download basemap quads that instersect with area of interest, and have controls such as date range and check for final coverage before download. The CLI also allows you to export the mosaics list as needed and can handle GeoJSON and KML files, and includes a tool to convert shapefiles to GeoJSON files for use with this tool.

### mosaic list
This tool allows you to pass a input geometry such as a GeoJSON or a KML file along with the start and end dates. It prints out the mosaic name, id and resolution. It prints out these information on the screen and the id could then be used to download the geotiffs.

```
usage: pbasemap mosaic_list [-h] [--geometry GEOMETRY] [--start START]
                            [--end END]

optional arguments:
  -h, --help           show this help message and exit
  --geometry GEOMETRY  Choose a geometry file supports GeoJSON, KML
  --start START        Choose Start date in format YYYY-MM-DD
  --end END            Choose End date in format YYYY-MM-DD
```

### download mosaic
As the name suggests this downloads your mosaic to the local folder you specify, you can specify how much coverage you want over your geometry and over the quad. So you may decide to only download those mosaic quads that have coverage more than 90% by simply specifying ```--coverage 90``` in the arguments.

```
usage: pbasemap download [-h] [--id ID] [--geometry GEOMETRY] [--local LOCAL]
                         [--coverage COVERAGE]

optional arguments:
  -h, --help           show this help message and exit
  --id ID              Mosaic ID from earlier search
  --geometry GEOMETRY  Choose a geometry file supports GeoJSON, KML
  --local LOCAL        Local folder to download images

Optional named arguments:
  --coverage COVERAGE  Choose minimum percentage coverage
```

### multipart download mosaic
This uses a multipart downloader to download your mosaic to the local folder you specify, you can specify how much coverage you want over your geometry and over the quad. So you may decide to only download those mosaic quads that have coverage more than 90% by simply specifying ```--coverage 90``` in the arguments.

```
usage: pbasemap mpdownload [-h] [--id ID] [--geometry GEOMETRY]
                           [--local LOCAL] [--coverage COVERAGE]

optional arguments:
  -h, --help           show this help message and exit
  --id ID              Mosaic ID from earlier search
  --geometry GEOMETRY  Choose a geometry file supports GeoJSON, KML
  --local LOCAL        Local folder to download images

Optional named arguments:
  --coverage COVERAGE  Choose minimum percentage coverage
```

### download mosaic metadata
Though typically the mosaic quads don't come with metadata, I decided to create metadata using the json response and some of the custom fields I though would be useful and this tool allows you to download that.

```
usage: pbasemap metadata [-h] [--geometry GEOMETRY] [--start START]
                         [--end END] [--output OUTPUT]

optional arguments:
  -h, --help           show this help message and exit
  --geometry GEOMETRY  Choose a geometry file supports GeoJSON, KML
  --start START        Choose Start date in format YYYY-MM-DD
  --end END            Choose End date in format YYYY-MM-DD
  --output OUTPUT      Full path where you want the metadata exported

```

### shape to geojson
This tool allows you to convert from  a folder with multiple shapefiles to a folder with geojson that can then be used with the tool. It makes use of geopandas and reprojects your shapefile to make it compatible while passing onto the API for search and download.

```
usage: pbasemap shp2geojson [-h] [--source SOURCE] [--destination DESTINATION]

optional arguments:
  -h, --help            show this help message and exit
  --source SOURCE       Choose Source Folder
  --destination DESTINATION
                        Choose Destination Folder
```

## Changelog

### v0.0.5

- Complete change to the codebase and underlying methodology
- Optimized code for search and download
- Overall improvements to code and major revisions

### v0.0.4

- Fixed projection issue for shapefiles
- Optimized code for shapefile to geojson export
- Overall improvements to code and minor revisions
