from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session
from core.security import generate_password_hash
from models import User
from schemas.user_schema import UserSchema, CreateUserSchema

user_router = APIRouter()

async def verify_cpf_exists(cpf: str, session: AsyncSession):
    result = await session.execute(select(User).filter(User.cpf == cpf))
    user = result.scalar()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Já existe um usuário com esse cpf!')


async def verify_email_exists(email: str, session: AsyncSession):
    result = await session.execute(select(User).filter(User.email == email))
    user = result.scalar()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Já existe um usuário com esse email!')



@user_router.post('/', response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
        user: CreateUserSchema,
        session: AsyncSession = Depends(get_session)
):
    await verify_cpf_exists(user.cpf, session)
    await verify_email_exists(user.email, session)
    new_user = User(
        fullName=user.fullName,
        email=user.email,
        cpf=user.cpf,
        phone=user.phone,
        password=generate_password_hash(user.password),
        role=user.role
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user
