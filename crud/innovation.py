from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import desc, extract, func, union_all, literal, Numeric
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, date
from typing import Optional
from schema.schemas import InnovationCreate, InnovationUpdate
from models import models
from database.database import get_db

# Custom Exception class
class ValidationException(Exception):
    def __init__(self, detail: str, status_code: int):
        self.detail = detail
        self.status_code = status_code

# Create new Innovation
def create_innovation(innovation_data: InnovationCreate, db: Session, current_innovator: models.Innovator):
    try:
        # Create the SQLAlchemy model from innovation data
        new_innovation = models.Innovation(
            course_name=innovation_data.course_name,
            course_description=innovation_data.course_description,
            content=innovation_data.content,
            course_duration=innovation_data.course_duration,
            course_price=innovation_data.course_price,
            course_image_path=innovation_data.course_image_path,
            course_domain=innovation_data.course_domain,
            created_at=datetime.now(),
            learners=innovation_data.learners
        )

        # Add new innovation to database session
        db.add(new_innovation)

        # Try to commit new innovation
        try:
            db.commit()
            db.refresh(new_innovation)
            return new_innovation
        
        except ValidationError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except SQLAlchemyError as e:
            db.rollback()
            if isinstance(e.__cause__, ValidationError):
                if isinstance(e.__cause__, ValidationError):
                    raise HTTPException(
                      status_code=status.HTTP_400_BAD_REQUEST,
                      detail=str(e.__cause__)
                    )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {str(e)}"
                )
    except Exception as e:
        if 'db' in locals() and db.is_active:
            db.rollback()
            raise HTTPException(
              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
              detail=f"Error creating sales entry: {str(e)}"
            )

# Retrieve innovation by name
def get_innovation_by_name(course_name: str, db: Session, current_innovator: models.Innovator):
    innovation_by_name = db.query(models.Innovation).filter(models.Innovation.course_name == course_name).first()

    return innovation_by_name

# Get all innovations belonging to a particular domain
def get_all_innovations_by_domain(course_domain: str, db: Session, current_innovator: models.Innovator):
    innovations_by_domain = db.query(models.Innovation).filter(models.Innovation.course_domain == course_domain).all()

    return innovations_by_domain

# Retrieve the list of innovators making an innovation
def get_innovators_on_innovation(course_name: str, db: Session, current_innovator: models.Innovator):
    innovators_on_innovation = db.query(models.Innovation)\
                                       .filter(models.Innovation.course_name == course_name)\
                                       .options(selectinload(models.Innovation.learners))\
                                       .first()

    if innovators_on_innovation:
        return innovators_on_innovation.learners
    else:
        return None

# Get all innovations
def get_all_innovations(db: Session, current_innovator: models.Innovator, skip: int = 0, limit: int = 100):
    innovations = db.query(models.Innovation).all()

    return innovations

# Update innovations
def update_innovations(course_name: str, innovation_data: InnovationUpdate, db: Session, current_innovator: models.Innovator):
    try:
        course_to_update = db.query(models.Innovation).filter(models.Innovation.course_name == course_name).first()

        if not course_to_update:
            raise ValueError(f"Course by name {course_name} not found.")

        course_data = innovation_data.model_dump()
        for key, value in course_data.items():
            setattr(course_to_update, key, value)

        course_to_update.created_at = datetime.now()
        db.commit()
        db.refresh(course_to_update)

        return course_to_update

    except Exception as e:
        if 'db' in locals() and db.is_active:
            db.rollback()
            raise HTTPException(
              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
              detail=f"Error updating innovation: {str(e)}"
            )

# delete innovation
def delete_innovation(course_name: str, db: Session, current_innovator: models.Innovator):
    try:
        course_to_delete = db.query(models.Innovation).filter(models.Innovation.course_name == course_name).first()

        if not course_to_delete:
            raise ValueError(f"Course by name {course_name} not found.")

        db.delete(course_to_delete)
        db.commit()

        return course_to_delete

    except Exception as e:
        if 'db' in locals() and db.is_active:
            db.rollback()
            raise HTTPException(
              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
              detail=f"Error deleting innovation: {str(e)}"
            )

        
        
        
