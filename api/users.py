from typing import List

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_setup import async_get_db
from pydantic_schemas.user import UserCreate, User
from api.utils.users import get_user, get_user_by_email, get_users, create_user, delete_user
from api.utils.courses import get_student_courses, get_teacher_courses
from pydantic_schemas.course import Course

router = fastapi.APIRouter()


@router.get("/students/{student_id}/courses", response_model=List[Course])
async def read_student_courses(student_id: int, db: AsyncSession = Depends(async_get_db)):
    db_student = await get_user(db=db, user_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_student.role == 1:
        raise HTTPException(status_code=400, detail="User is not a student")
    student_courses = await get_student_courses(db=db, student_id=student_id)
    return [i[0] for i in student_courses]

@router.get("/teachers/{teacher_id}/courses", response_model=List[Course])
async def read_teacher_courses(teacher_id: int, db: AsyncSession = Depends(async_get_db)):
    db_teacher = await get_user(db=db, user_id=teacher_id)
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_teacher.role == 2:
        raise HTTPException(status_code=400, detail="User is not a teacher")
    teacher_courses = await get_teacher_courses(db=db, teacher_id=teacher_id)
    return [i[0] for i in teacher_courses]


@router.get("/users", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(async_get_db)):
    users = await get_users(db, skip=skip, limit=limit)
    return [i[0] for i in users]


@router.post("/users", response_model=User, status_code=201)
async def create_new_user(user: UserCreate, db: AsyncSession = Depends(async_get_db)):
    db_user = await get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered")
    return await create_user(db=db, user=user)


@router.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int, db: AsyncSession = Depends(async_get_db)):
    db_user = await get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/users/{user_id}", status_code=204)
async def remove_user(user_id: int, db: AsyncSession = Depends(async_get_db)):
    db_user = await get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await delete_user(db=db, user_id=user_id)
