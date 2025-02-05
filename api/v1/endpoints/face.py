import logging
import os
import aiofiles
import cv2
import face_recognition
from sqlalchemy.future import select

from api.v1.endpoints.logs import log_event
from schemas.ticket_schema import TicketSchema
from fastapi import File, UploadFile, APIRouter, Depends, HTTPException, status, Form
from minio import Minio
from minio.error import S3Error
from sqlalchemy.ext.asyncio import AsyncSession
from models import Ticket
from core.deps import get_session

# Carregar o classificador de rosto do OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

face_router = APIRouter()

# Configurar o cliente MinIO
minio_client = Minio(
    "mesquitadev-minio.mp1rvc.easypanel.host",  # Substitua pelo seu endpoint MinIO
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=True  # Defina como True se estiver usando HTTPS
)

bucket_name = "fauves"  # Substitua pelo nome do seu bucket

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@face_router.post("/upload-image/", response_model=TicketSchema, status_code=status.HTTP_201_CREATED)
async def upload_image(
    user_id: str = Form(...),
    email: str = Form(...),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session)
):
    try:
        # Save the image temporarily
        temp_file_path = f"temp_{file.filename}"
        async with aiofiles.open(temp_file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)

        # Read the image using OpenCV
        img = cv2.imread(temp_file_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Check if there is more than one face in the image
        if len(faces) != 1:
            os.remove(temp_file_path)
            await log_event(session, "upload_image_error", user_id, "A imagem deve conter exatamente um rosto")
            raise HTTPException(status_code=400, detail="A imagem deve conter exatamente um rosto")

        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Save the processed image
        processed_file_path = f"processed_{file.filename}"
        cv2.imwrite(processed_file_path, img)

        # Upload the processed image to MinIO
        minio_client.fput_object(bucket_name, processed_file_path, processed_file_path)

        # Remove the temporary file
        os.remove(temp_file_path)

        # Construct the HTTPS URL of the uploaded image
        image_url = f"https://mesquitadev-minio.mp1rvc.easypanel.host/{bucket_name}/{processed_file_path}"

        new_ticket = Ticket(
            image_url=image_url,
            user_id=user_id,
            email=email
        )
        session.add(new_ticket)
        await session.commit()
        await session.refresh(new_ticket)

        # Remove the processed file
        os.remove(processed_file_path)

        await log_event(session, "upload_image_success", user_id, f"URL da imagem: {image_url}")

        return new_ticket

    except Exception as e:
        await session.rollback()  # Rollback the session before logging the error
        await log_event(session, "upload_image_error", user_id, str(e))
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro durante o upload da imagem: {str(e)}")

@face_router.post("/verify-image/")
async def verify_image(
    user_id: str = Form(...),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session)
):
    try:
        # Obter o ticket do banco de dados usando user_id
        ticket = await session.execute(
            select(Ticket).where(Ticket.user_id == user_id)
        )
        ticket = ticket.scalars().first()
        if not ticket:
            await log_event(session, "verify_image_error", user_id, "Ticket não encontrado")
            raise HTTPException(status_code=404, detail="Cliente não identificado")

        # Baixar a imagem original do MinIO
        original_image_path = f"original_{ticket.image_url.split('/')[-1]}"
        try:
            minio_client.fget_object(bucket_name, ticket.image_url.split('/')[-1], original_image_path)
        except S3Error as e:
            await log_event(session, "verify_image_error", user_id, str(e))
            raise HTTPException(status_code=500, detail=str(e))

        # Salvar a nova imagem temporariamente
        temp_file_path = f"temp_{file.filename}"
        async with aiofiles.open(temp_file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)

        # Carregar as imagens usando face_recognition
        original_image = face_recognition.load_image_file(original_image_path)
        new_image = face_recognition.load_image_file(temp_file_path)

        # Obter as codificações faciais das imagens
        original_encoding = face_recognition.face_encodings(original_image)
        new_encoding = face_recognition.face_encodings(new_image)

        # Verificar se há exatamente um rosto em cada imagem
        if len(original_encoding) != 1 or len(new_encoding) != 1:
            os.remove(original_image_path)
            os.remove(temp_file_path)
            await log_event(session, "verify_image_error", user_id, "Cada imagem deve conter exatamente um rosto")
            raise HTTPException(status_code=400, detail="Cada imagem deve conter exatamente um rosto")

        # Comparar as codificações faciais
        match = face_recognition.compare_faces([original_encoding[0]], new_encoding[0])[0]

        # Remover os arquivos temporários
        os.remove(original_image_path)
        os.remove(temp_file_path)

        # Converter numpy.bool_ para bool
        match = bool(match)

        # Adicionar mensagem ao retorno
        message = "Identidade confirmada" if match else "Identidade não confirmada"

        await log_event(session, "verify_image_success", user_id, message)

        return {"match": match, "message": message}

    except Exception as e:
        await session.rollback()  # Rollback the session before logging the error
        await log_event(session, "verify_image_error", user_id, str(e))
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro durante a verificação da imagem: {str(e)}")