from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .mixins import Timestamp
from db.models import base

class StudentCourse(Timestamp, base.Base):
    __tablename__ = "student_courses"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="cascade"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="cascade"), nullable=False)

    student = relationship("User", back_populates="student_courses")
    course = relationship("Course", back_populates="student_courses")
