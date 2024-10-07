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


def delete_geojson_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False
