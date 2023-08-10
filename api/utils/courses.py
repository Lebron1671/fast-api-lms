from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.course import Course
from db.models.student_course import StudentCourse
from db.models.user import User
from pydantic_schemas.course import CourseCreate


async def create_course(db: AsyncSession, course: CourseCreate):
    db_course = Course(
        title=course.title,
        description=course.description,
        academic_hours=course.academic_hours,
        classroom=course.classroom,
        teacher_id=course.teacher_id
    )
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    return db_course


async def get_course(db: AsyncSession, course_id: int):
    query = select(Course).where(Course.id == course_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_courses(db: AsyncSession):
    query = select(Course)
    result = await db.execute(query)
    return result.fetchall()


async def update_course(course_id: int, db: AsyncSession, course: CourseCreate):
    db_course = await get_course(db, course_id)
    for field, value in course.model_dump().items():
        setattr(db_course, field, value)

    await db.commit()
    await db.refresh(db_course)
    return db_course


async def delete_course(db: AsyncSession, course_id: int):
    db_course = await get_course(db, course_id)
    await db.delete(db_course)
    await db.commit()
    return db_course


async def add_user_to_course(db: AsyncSession, course_id:int, student_id: int):
    db_student_course = StudentCourse(
        student_id=student_id,
        course_id=course_id
    )
    db.add(db_student_course)
    await db.commit()
    await db.refresh(db_student_course)
    return db_student_course


async def add_teacher_to_course(db: AsyncSession, course_id: int, teacher_id: int):
    db_course = await get_course(db, course_id)
    db_course.teacher_id = teacher_id
    await db.commit()
    await db.refresh(db_course)
    return db_course


async def get_student_courses(db: AsyncSession, student_id: int):
    query = select(Course).join(StudentCourse, StudentCourse.course_id == Course.id)\
                          .where(StudentCourse.student_id == student_id)
    result = await db.execute(query)
    return result.fetchall()


async def get_course_students(db: AsyncSession, course_id: int):
    query = select(User).join(StudentCourse, StudentCourse.student_id == User.id) \
        .where(StudentCourse.course_id == course_id)
    result = await db.execute(query)
    return result.fetchall()


async def get_teacher_courses(db: AsyncSession, teacher_id: int):
    query = select(Course).where(Course.teacher_id == teacher_id)
    result = await db.execute(query)
    return result.fetchall()


# def get_teacher_courses(db: Session, teacher_id: int):
#     courses = db.query(Course).filter(Course.teacher_id == teacher_id).all()
#     return courses

# def create_course(db: Session, course: CourseCreate):
#     db_course = Course(
#         title=course.title,
#         description=course.description,
#         academic_hours=course.academic_hours,
#         classroom=course.classroom,
#         teacher_id=course.teacher_id
#     )
#     db.add(db_course)
#     db.commit()
#     db.refresh(db_course)
#     return db_course


# def get_course(db: Session, course_id: int):
#     return db.query(Course).filter(Course.id == course_id).first()


# def get_courses(db: Session):
#     return db.query(Course).all()


# def get_student_courses(db: Session, student_id: int):
#     courses = (
#         db.query(Course)
#         .join(StudentCourse, StudentCourse.course_id == Course.id)
#         .filter(StudentCourse.student_id == student_id)
#         .all()
#     )
#     return courses


# def get_course_students(db: Session, course_id: int):
#     students = (
#         db.query(User)
#         .join(StudentCourse, StudentCourse.student_id == User.id)
#         .filter(StudentCourse.course_id == course_id)
#         .all()
#     )
#     return students


# def add_user_to_course(db: Session, course_id:int, student_id: int):
#     db_student_course = StudentCourse(
#         student_id=student_id,
#         course_id=course_id
#     )
#     db.add(db_student_course)
#     db.commit()
#     db.refresh(db_student_course)
#     return db_student_course

# def add_teacher_to_course(db: Session, course_id: int, teacher_id: int):
#     db_course = db.query(Course).filter(Course.id == course_id).first()
#
#     if db_course:
#         db_course.teacher_id = teacher_id
#         db.commit()
#         db.refresh(db_course)
#
#     return db_course

# def delete_course(db: Session, course_id: int):
#     db_course = db.query(Course).filter(Course.id == course_id).first()
#
#     if db_course:
#         db.delete(db_course)
#         db.commit()
#
#     return db_course


