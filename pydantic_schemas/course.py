from typing import Optional

from pydantic import BaseModel


class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    academic_hours: int
    classroom: Optional[str] = None
    teacher_id: Optional[int] = None


class CourseCreate(CourseBase):
    ...


class Course(CourseBase):
    id: int

    class Config:
        from_attributes = True
