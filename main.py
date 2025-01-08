# import os
#
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse

from api.v1.endpoints.auth import auth_router
from api.v1.endpoints.users import user_router

#
# import mapas
# from core.database import Base, engine
# from models import apiary, meliponary, user
# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# @app.post("/upload-geojson/")
# async def upload_geojson(files: list[UploadFile] = File(...)):
#     file_paths = [mapas.save_geojson_file(file) for file in files]
#     return JSONResponse(content={"filenames": file_paths})
#
# @app.get("/list-geojson/")
# async def list_geojson():
#     files = mapas.list_geojson_files()
#     return JSONResponse(content={"files": files})
#
# @app.get("/geojson-content/{filename}")
# async def geojson_content(filename: str):
#     content = mapas.get_geojson_file_content(filename)
#     if content is None:
#         return JSONResponse(content={"error": "File not found"}, status_code=404)
#     return JSONResponse(content=content)
#
#
# @app.get("/geojson-content/{filename}")
# async def geojson_content(filename: str):
#     file_path = os.path.join(mapas.UPLOAD_DIR, filename)
#     if not os.path.exists(file_path):
#         return JSONResponse(content={"error": "File not found"}, status_code=404)
#
#     def iterfile():
#         with open(file_path, "r") as file:
#             for line in file:
#                 yield line
#
#     return StreamingResponse(iterfile(), media_type="application/json")
#
# @app.delete("/delete-geojson/{filename}")
# async def delete_geojson(filename: str):
#     success = mapas.delete_geojson_file(filename)
#     if not success:
#         raise HTTPException(status_code=404, detail="File not found")
#     return JSONResponse(content={"message": "File deleted successfully"})

from api.v1.endpoints.meliponary import meliponary_router

app.include_router(meliponary_router, prefix='/api/v1/meliponaries', tags=['meliponaries'])
app.include_router(user_router, prefix='/api/v1/users', tags=['users'])
app.include_router(auth_router, prefix='/api/v1/auth', tags=['Authenticate'])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level='info', reload=True)