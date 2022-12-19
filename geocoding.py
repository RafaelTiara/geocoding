# -*- coding: utf-8 -*-

import pandas as pd
import os
from pyproj import Transformer
from urllib.parse import urlencode
import requests

#%% 1. SET PATHS
os.chdir(r'C:\Users\rtiara\Downloads\Housing Externalities - Rafael Tiara v2\Housing Externalities - Rafael Tiara v2')
OR_DATA_DIR = '1_data/1_raw/old data/BL_FUI.dta'
base = pd.read_excel(OR_DATA_DIR)
DESTINATION_DATA_DIR = '1_data/2_intermediate/base_v1.xlsx'

for i in range(len(base)):
    direccion=str(base.at[i, 'calle_avenida_pasaje'])+' '+str(base.at[i, 'numero'])+', '+str(base.at[i, 'comuna'])+', Región Metropolitana, Chile'
    base.at[i, 'direccion'] = direccion
    print(direccion)

#%%
def reproyect(lat, lng):
    trans = Transformer.from_crs('epsg:4326', 'epsg:3857')
    lat, lng = trans.transform(lat, lng)
    return lat, lng

#2. Obtener coordenadas de Google Maps con direcciones de hogares
api_key = 

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

#%%
for i in range(len(base)):
    direccion = base.at[i, 'direccion']
    try:
        extraccion = extract_lat_lng(direccion)
        reproyeccion = reproyect(extraccion['lat'], extraccion['lng'])
        base.at[i, 'latitud_geocode'], base.at[i, 'longitud_geocode'] = reproyeccion
    except:
        pass
    print(direccion)

#%%
base.to_excel(DESTINATION_DATA_DIR)
