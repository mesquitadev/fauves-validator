from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from core.auth import authenticate, generate_token, create_access_token
from core.deps import get_session

auth_router = APIRouter()


@auth_router.post('/login', status_code=status.HTTP_201_CREATED)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    user = await authenticate(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Credenciais inválidas')
    return JSONResponse(content={'access_token': create_access_token(sub=str(user.id)), "token_type": "bearer"}, status_code=status.HTTP_200_OK)
