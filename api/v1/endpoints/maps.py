from typing import List
from urllib.request import Request

from fastapi import APIRouter, Depends, status, HTTPException, Response, UploadFile, File
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import os
import shutil
import json

from core.deps import get_session, get_current_user
from models import User, Maps
from models.meliponary import Meliponary
from schemas.meliponary_schema import MeliponaryCreateSchema, MeliponarySchema
from utils import verify_user_exists

maps_router = APIRouter()
UPLOAD_DIR = "geojson_files"
BASE_URL = os.getenv('BASE_URL')


@maps_router.post("/upload/")
async def upload_geojson(files: List[UploadFile] = File(...), session: AsyncSession = Depends(get_session)):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    file_paths = []
    for file in files:
        lowercase_filename = file.filename.lower()
        file_path = os.path.join(UPLOAD_DIR, lowercase_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_paths.append(file_path)

        # Save file data to the database
        new_map = Maps(file_path=file_path, name=file.filename)
        session.add(new_map)

    await session.commit()
    return JSONResponse(content={"file_paths": file_paths})

@maps_router.get("/")
async def list_geojson(session: AsyncSession = Depends(get_session)):
    async with session.begin():
        result = await session.execute(select(Maps))
        maps = result.scalars().all()

    file_urls = [{"id": map.id, "name": map.name, "url": f"{BASE_URL}/api/v1/maps/content/{os.path.basename(map.file_path)}"} for map in maps]
    return JSONResponse(content=file_urls)

@maps_router.get("/content/{filename}")
async def geojson_content(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        return JSONResponse(content={"error": "File not found"}, status_code=404)
    with open(file_path, "r") as file:
        content = json.load(file)
    return JSONResponse(content=content)


@maps_router.delete("/{map_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_geojson(map_id: int, session: AsyncSession = Depends(get_session)):
    async with session.begin():
        result = await session.execute(select(Maps).filter(Maps.id == map_id))
        map_entry = result.scalar()

        if not map_entry:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Map not found")

        # Delete the file from the file system
        file_path = map_entry.file_path
        if os.path.exists(file_path):
            os.remove(file_path)

        # Delete the map entry from the database
        await session.delete(map_entry)
        await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)