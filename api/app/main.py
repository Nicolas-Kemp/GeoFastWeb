from fastapi import FastAPI, Query
from fastapi import Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware  # NEW
import geopandas as gpd
import pandas as pd
import numpy as np
from datetime import datetime
from shapely.geometry import box, Polygon
import h3
import app.threed_functions as tf
import os
import json
import yaml
from urllib.parse import quote_plus
from sqlalchemy import create_engine


dirname = os.path.dirname(__file__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root(text: str = ' '):
    return {"Hello": "From the other side" + text}


@app.get("/threetiff")
def threetif_api(default_tiff: str='tablemountain.tiff'):
    tiff_toget = os.path.join(dirname, 'static/tiff/'+default_tiff)
    dict_toget = tf.import_spatial_layer(tiff_toget, "aoi").object_dict()

    return json.dumps(dict_toget)

@app.get("/geotripz")
async def geotripz_api( love_it: str = '',
                        like_it: str = '',
                        rather_not: str = '',
                        noway: str = ''):
    
    lst_loveit = [item for item in love_it.split(",") if item != '']
    lst_likeit = [item for item in like_it.split(",") if item != '']
    lst_rathernot = [item for item in rather_not.split(",") if item != '']
    lst_noway = [item for item in noway.split(",") if item != '']

    lst_normalised_fields = lst_loveit + lst_likeit + lst_rathernot + lst_noway


    print('hello_geotripz')
    with open('app/config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    db_password = config['db_password']
    db_host = config['db_host']

    import psycopg2
    con = psycopg2.connect(database='geoserver',
                    user='geoserver',
                    password=db_password,
                    host='general-pg-aurora-development.cluster-camvfnd8svoc.af-south-1.rds.amazonaws.com')

    sql = """SELECT * FROM demo.geotripz_h3_grid"""

    # Layer from Postgis
    geotripz_layer_to_norm = gpd.read_postgis(sql, con, geom_col='geometry')


    dbschema='demo' # Searches left-to-right
    engine = create_engine(
    f'postgresql+psycopg2://geoserver:%s@{db_host}:5432/geoserver' % quote_plus(db_password))

    # add required fields
    lst_normalised_fields = lst_loveit + lst_likeit + lst_rathernot + lst_noway
    # calculate pristine hotspot score
    geotripz_layer_to_norm[lst_normalised_fields] = geotripz_layer_to_norm[lst_normalised_fields].apply(lambda x: (x - x.min()) / (x.max() - x.min())).fillna(0)
    loveit_val = geotripz_layer_to_norm[lst_loveit].sum(axis=1)*5
    likeit_val = geotripz_layer_to_norm[lst_likeit].sum(axis=1)*2
    rathernot_val = geotripz_layer_to_norm[lst_rathernot].sum(axis=1)*-2
    noway_val = geotripz_layer_to_norm[lst_noway].sum(axis=1)*-999
    geotripz_layer_to_norm['geotripz_score'] = loveit_val+likeit_val+rathernot_val+noway_val

    # replace h3 grids with no value where pristine hotspot score is zero or smaller
    geotripz_layer_to_norm.loc[geotripz_layer_to_norm['geotripz_score'] <=0, 'geotripz_score'] = np.NaN

    # replace h3 grids with no value where there is no love-it score
    geotripz_layer_to_norm.loc[loveit_val <=0, 'geotripz_score'] = np.NaN

    # label prestine hotspots based on quantiles
    lst_score_quantiles = list(geotripz_layer_to_norm['geotripz_score'].quantile([.3, .6, 0.85, 0.98, 1]))
    geotripz_layer_to_norm['geotripz_score_tag'] = pd.cut(geotripz_layer_to_norm['geotripz_score'], lst_score_quantiles, labels=["4_Not much, but there is something", "3_Might be worth while", "2_Recomended", "1_Highly recomended"])
    geotripz_layer_to_norm['geotripz_score_tag'] = geotripz_layer_to_norm.geotripz_score_tag.astype(str)
    geotripz_layer_to_norm['geotripz_score_tag'] = geotripz_layer_to_norm['geotripz_score_tag'].fillna('0_NA')

    # remove rows where pristine hotspots have no values
    geotripz_layer_to_norm = geotripz_layer_to_norm.dropna(subset=['geotripz_score'])

    # write to postgis
    geotripz_layer_to_norm.to_postgis("geotripz_h3_output", engine, schema='demo', if_exists='replace')


@app.get("/h3_on_the_fly")
async def h3_on_the_fly_api(bottom_lat: float = -35.04,
                            top_lat: float = -22.04,
                            left_long: float = 14.97,
                            right_long: float = 34.92,
                        z_level: int = 3,
                        return_type: str = ''):
    
    bounding_box = [left_long, bottom_lat, right_long, top_lat]

    print(bounding_box)
    bbox_order = [0, 1, 2, 3]
    bbox = [bounding_box[i] for i in bbox_order]

    print(z_level)
    geom = box(*bbox)
    z_level = int(z_level)

    if z_level > 12:
        z_level = 9
    elif z_level == 12:
        z_level = 8
    elif z_level <= 11 and z_level >= 10:
        z_level = 7
    elif z_level <= 9 and z_level >= 8:
        z_level = 6
    elif z_level <= 7 and z_level >= 6:
        z_level = 5
    elif z_level <= 5 and z_level >= 4:
        z_level = 4
    elif z_level == 4:
        z_level = 3
    elif z_level == 3:
        z_level = 3
    elif z_level == 2:
        z_level = 2
    elif z_level <= 1:
        z_level = 1

    hexs = h3.polyfill(geom.__geo_interface__, z_level, geo_json_conformant=True)

    polygonise = lambda hex_id: Polygon(
                                        h3.h3_to_geo_boundary(
                                            hex_id, geo_json=True)
                                        )

    json_h3_on_the_fly = gpd.GeoSeries(list(map(polygonise, hexs)),
                                       index=hexs,
                                       crs="EPSG:4326"
                                       ).to_json()

    if return_type == 'json':
        return Response(content=json_h3_on_the_fly, media_type="application/json")
    else:
        return json_h3_on_the_fly