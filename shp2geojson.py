import shapefile
import os
def shp2gj(folder,export):
    for items in os.listdir(folder):
        if items.endswith('.shp'):
            reader = shapefile.Reader(os.path.join(folder,items))
            fields = reader.fields[1:]
            field_names = [field[0] for field in fields]
            buffer = []
            for sr in reader.shapeRecords():
               atr = dict(zip(field_names, sr.record))
               geom = sr.shape.__geo_interface__
               buffer.append(dict(type="Feature", \
                geometry=geom, properties=atr)) 

            # write the GeoJSON file
            from json import dumps
            geojson = open(os.path.join(export,str(items).replace('.shp','.geojson')), "w")
            geojson.write(dumps({"type": "FeatureCollection",\
            "features": buffer}, indent=2) + "\n")
            geojson.close()
#shp2gj(folder=r"C:\Users\samapriya\Downloads\nexgengrid")
