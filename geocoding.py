# -*- coding: utf-8 -*-
# This code uses Google Maps API to extract coordinates using Household's addresses and create shapefiles to help visualization
import pandas as pd
import os
from pyproj import Transformer
from urllib.parse import urlencode
import requests

#%% 1. SET PATHS
os.chdir(r'C:\Users\rtiara\Downloads\Housing Externalities - Rafael Tiara v2\Housing Externalities - Rafael Tiara v2')
OR_DATA_DIR = '1_data/1_raw/old data/BL_FUI.dta'
base = pd.read_excel(OR_DATA_DIR)
DESTINATION_DATA_DIR = '1_data/2_intermediate/base.xlsx'

#1. Get addresses in Google Maps Format
for i in range(len(base)):
    direccion=str(base.at[i, 'calle_avenida_pasaje'])+' '+str(base.at[i, 'numero'])+', '+str(base.at[i, 'comuna'])+', Región Metropolitana, Chile'
    base.at[i, 'direccion'] = direccion
    print(direccion)

#2. Define some functions
#Reproyect from EPSG:4326 (in degrees) to EPSG:3857 (in mts)
def reproyect(lat, lng):
    trans = Transformer.from_crs('epsg:4326', 'epsg:3857')
    lat, lng = trans.transform(lat, lng)
    return lat, lng

#2. Enter GOOGLE MAPS API KEY
api_key = 

#3. Extraction process
def extract_lat_lng(address, data_type = 'json'):
    #GOOGLE API SEARCH ADDRESSES
    endpoint = f'https://maps.googleapis.com/maps/api/geocode/{data_type}'
    params = {'address': address, 'key': api_key}
    url_params = urlencode(params)
    url = f"{endpoint}?{url_params}"
    r = requests.get(url)
    if r.status_code not in range(200, 299):
        return {}
    latlng = {}
    try:
        return r.json()['results'][0]['geometry']['location']
    except:
        pass
    return latlng.get('lat'), latlng.get('lng')

#4. Reproject
for i in range(len(base)):
    direccion = base.at[i, 'direccion']
    try:
        extraccion = extract_lat_lng(direccion)
        reproyeccion = reproyect(extraccion['lat'], extraccion['lng'])
        base.at[i, 'latitud_geocode'], base.at[i, 'longitud_geocode'] = reproyeccion
    except:
        pass
    print(direccion)
    
#5. Create a GeoDataFrame
def to_geodata(base, latitud, longitud):
    data = pd.DataFrame('', columns = ['id', 'geometry'], index = np.arange(0, len(base)))
    for i in range(len(data)):
        #Creamos puntos
        if math.isnan(base.at[i, latitud]) == True:
            data.at[i, 'geometry'] = 'PUNTO-VACIO'
        elif math.isnan(base.at[i, latitud]) == False:
            punto = Point(base.at[i, longitud], base.at[i, latitud])
            data.at[i,'id'] = i
            data.at[i,'geometry'] = punto
    data = data[data['geometry'] != 'PUNTO-VACIO']
    # A geodataframe
    geodata = gdp.GeoDataFrame(data, geometry = 'geometry')
    return(geodata)

#6. Define function to save as Shapefile
def to_shape(geodata, nombre):
    geodata.to_file(str(nombre) + ".shp")
    
geobase = to_geodata(base, 'latitud_geocode', 'longitud_geocode')

#7. Saving
to_shape(geobase, 'Shapefiles/coordenadas_hogares')
base.to_excel(DESTINATION_DATA_DIR)
