from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.models.user import User
from pydantic_schemas.user import UserCreate


async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(
        email=user.email,
        role=user.role,
        first_name=user.first_name,
        last_name=user.last_name,
        birthday=user.birthday,
        phone=user.phone
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user(db: AsyncSession, user_id: int):
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str):
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    query = select(User).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.fetchall()


async def update_user(db: AsyncSession, user_id: int, user: UserCreate):
    db_user = await get_user(db, user_id)
    for field, value in user.model_dump().items():
        setattr(db_user, field, value)

    db_user.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int):
    db_user = await get_user(db, user_id)
    await db.delete(db_user)
    await db.commit()
    return db_user
