import enum

from sqlalchemy import Boolean, Column, Integer, String, Enum, Date
from sqlalchemy.orm import relationship

from .mixins import Timestamp
from db.models import base

class Role(enum.IntEnum):
    teacher = 1
    student = 2

class User(Timestamp, base.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    birthday = Column(Date, nullable=False)
    phone = Column(String(20), nullable=True)
    role = Column(Enum(Role))
    is_active = Column(Boolean, default=True)

    student_courses = relationship("StudentCourse", back_populates="student", cascade="all, delete", passive_deletes=True)
    course = relationship("Course", back_populates="student")
