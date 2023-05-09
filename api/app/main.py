from fastapi import FastAPI, Query
from fastapi import Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware  # NEW
import geopandas as gpd
from datetime import datetime
from shapely.geometry import box, Polygon
import h3

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