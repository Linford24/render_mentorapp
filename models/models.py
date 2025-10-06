from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, event, UUID, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.postgresql import JSONB
from database.database import Base
import hashlib
import uuid

# Association Table for Many-to-Many relationship
# This table will link Innovators to Innovations they have registered for.
innovation_learner_association = Table(
    'innovation_learner_association',
    Base.metadata,
    Column("innovation_id", Integer, ForeignKey("innovation.id"), primary_key=True),
    Column("innovator_id", Integer, ForeignKey("innovators.id"), primary_key=True)
)


class Innovator(Base):
    __tablename__ = "innovators"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    status = Column(String, nullable=False)
    language = Column(String, nullable=False)
    date_joined = Column(DateTime(timezone=True), server_default=func.now())
    
    # Many-to-Many relationship: An Innovator can register for many Innovations
    # Use 'secondary' to specify the association table
    registered_courses = relationship(
        "Innovation", 
        secondary=innovation_learner_association,
        back_populates="learners")
    

class Innovation(Base):
    __tablename__ = "innovation"

    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String, unique=True, nullable=False)
    course_description = Column(String, nullable=False)
    content = Column(MutableDict.as_mutable(JSONB), nullable=True)
    course_duration = Column(Integer, nullable=False)
    course_price = Column(String, nullable=False)
    course_tutor = Column(String, nullable=False)
    course_image_path = Column(String, nullable=False)
    course_domain = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    learners = relationship(
        "Innovator", 
        secondary=innovation_learner_association,
        back_populates="registered_courses")


    