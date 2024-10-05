import json
import os
from fastapi import UploadFile
import shutil
from shapely.geometry import shape, box, mapping
from shapely.ops import transform
import gzip
import geojson
import pyproj

UPLOAD_DIR = "geojson_files"


def save_geojson_file(file: UploadFile):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    lowercase_filename = file.filename.lower()
    file_path = os.path.join(UPLOAD_DIR, lowercase_filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path


def list_geojson_files():
    if not os.path.exists(UPLOAD_DIR):
        return []
    return [f for f in os.listdir(UPLOAD_DIR) if f.endswith('.geojson')]


def get_geojson_file_content(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r") as file:
        return json.load(file)


def transform_geometry(geometry, from_crs="EPSG:4326", to_crs="EPSG:3857"):
    transformer = pyproj.Transformer.from_crs(from_crs, to_crs, always_xy=True)
    return transform(transformer.transform, shape(geometry))


def simplify_geometry(geometry, tolerance=0.01):
    return shape(geometry).simplify(tolerance)


def split_geojson(filename: str, max_features: int = 1000, bounds: str = None, tolerance: float = 0.01):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r") as file:
        data = geojson.load(file)

    if data['type'] != 'FeatureCollection':
        return None

    features = data['features']

    if bounds:
        min_lat, min_lng, max_lat, max_lng = map(float, bounds.split(','))
        bounding_box = box(min_lng, min_lat, max_lng, max_lat)
        features = [feature for feature in features if bounding_box.intersects(shape(feature['geometry']))]

    transformed_features = []
    for feature in features:
        transformed_geometry = transform_geometry(feature['geometry'])
        simplified_geometry = simplify_geometry(transformed_geometry, tolerance)
        feature['geometry'] = mapping(simplified_geometry)
        transformed_features.append(feature)

    chunks = [transformed_features[i:i + max_features] for i in range(0, len(transformed_features), max_features)]

    chunk_files = []
    for i, chunk in enumerate(chunks):
        chunk_data = {
            "type": "FeatureCollection",
            "features": chunk
        }
        chunk_file_path = os.path.join(UPLOAD_DIR, f"chunk_{i}_{filename}.geojson.gz")
        with gzip.open(chunk_file_path, "wt", encoding="utf-8") as file:
            geojson.dump(chunk_data, file)
        chunk_files.append(chunk_file_path)

    return chunk_files


def get_chunk_file_content(chunk_filename: str):
    chunk_file_path = os.path.join(UPLOAD_DIR, chunk_filename)
    if not os.path.exists(chunk_file_path):
        return None
    with gzip.open(chunk_file_path, "rt", encoding="utf-8") as file:
        return json.load(file)


def delete_geojson_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False
