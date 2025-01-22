# seed.py
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import engine
from core.security import generate_password_hash
from models.user import User

async def seed_data():
    async with AsyncSession(engine) as session:
        async with session.begin():
            # Add seed data for User
            password = generate_password_hash("12345678")
            user1 = User(fullName="Demonstração Meliponário", cpf="31312132", phone="asdasdasdasd", email="meli@geobee.app", password=password , role="APICULTOR")
            user2 = User(fullName="Demonstração Apiário", cpf="123123123", phone="asdasdasd", email="apic@geobee.app", password=password, role="MELIPONICULTOR")
            session.add_all([user1, user2])

            # # Add seed data for Maps
            # map1 = Maps(file_path="/path/to/map1", name="Map 1")
            # map2 = Maps(file_path="/path/to/map2", name="Map 2")
            # session.add_all([map1, map2])

        await session.commit()
        print("Seed data inserted successfully!")

if __name__ == '__main__':
    asyncio.run(seed_data())