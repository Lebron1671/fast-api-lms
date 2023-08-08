from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .mixins import Timestamp
from db.models import base

class Course(Timestamp, base.Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    academic_hours = Column(Integer, nullable=False)
    classroom = Column(String(200), nullable=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)


    student = relationship("User", back_populates="course")
    student_courses = relationship("StudentCourse", back_populates="course", cascade="all, delete", passive_deletes=True)
