from typing import List

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.users import get_user
from db.db_setup import async_get_db
from pydantic_schemas.course import CourseCreate, Course
from api.utils.courses import get_course, get_courses, create_course, delete_course, get_course_students, \
    add_user_to_course, add_teacher_to_course, get_student_courses, get_teacher_courses
from pydantic_schemas.user import User

router = fastapi.APIRouter()


@router.get("/courses", response_model=List[Course])
async def read_courses(db: AsyncSession = Depends(async_get_db)):
    courses = await get_courses(db=db)
    return [i[0] for i in courses]


@router.post("/courses", response_model=Course)
async def create_new_course(course: CourseCreate, db: AsyncSession = Depends(async_get_db)):
    return await create_course(db=db, course=course)


@router.get("/courses/{course_id}", response_model=Course)
async def read_course(course_id: int, db: AsyncSession = Depends(async_get_db)):
    db_course = await get_course(db=db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


@router.get("/users/{course_id}/users", response_model=List[User])
async def read_course_students(course_id: int, db: AsyncSession = Depends(async_get_db)):
    db_course = await get_course(db=db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    course_students = await get_course_students(db=db, course_id=course_id)
    return [i[0] for i in course_students]


@router.post("/courses/{course_id}/student", status_code=201)
async def assign_course_for_student(course_id: int, student_id: int, db: AsyncSession = Depends(async_get_db)):
    db_course = await get_course(db=db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    if db_course.teacher_id is None:
        raise HTTPException(status_code=400, detail="A teacher has not yet been appointed to this course")

    db_user = await get_user(db=db, user_id=student_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.role == 1:
        raise HTTPException(status_code=400, detail="User is not a student")

    db_student_courses = await get_student_courses(db=db, student_id=student_id)
    student_courses = [i[0] for i in db_student_courses]
    if any([row for row in student_courses if row.id == course_id]):
        raise HTTPException(status_code=400, detail="Student is already enrolled in this course")

    return await add_user_to_course(db=db, course_id=course_id, student_id=student_id)


@router.post("/courses/{course_id}/teacher", status_code=201)
async def assign_course_for_teacher(course_id: int, teacher_id: int, db: AsyncSession = Depends(async_get_db)):
    db_course = await get_course(db=db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    db_user = await get_user(db=db, user_id=teacher_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.role == 2:
        raise HTTPException(status_code=400, detail="User is not a teacher")

    db_teacher_courses = await get_teacher_courses(db=db, teacher_id=teacher_id)
    teacher_courses = [i[0] for i in db_teacher_courses]
    if any([row for row in teacher_courses if row.id == course_id]):
        raise HTTPException(status_code=400, detail="Teacher is already enrolled in this course")

    return await add_teacher_to_course(db=db, course_id=course_id, teacher_id=teacher_id)


@router.delete("/courses/{course_id}", status_code=204)
async def remove_course(course_id: int, db: AsyncSession = Depends(async_get_db)):
    db_course = await get_course(db=db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return await delete_course(db=db, course_id=course_id)


#
# @router.patch("/courses/{id}")
# async def update_course():
#     return {"courses": []}
