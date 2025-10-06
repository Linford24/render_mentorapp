from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import exc
import logging
from datetime import datetime
from schema.schemas import InnovatorCreate, InnovatorResponse, InnovatorUpdate, ShowInnovator
from models.models import Innovator as InnovatorModel
from crud import hashing

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create innovator
def create_innovator(innovator_data: InnovatorCreate, db: Session) -> InnovatorResponse:
    try:
        # Check if innovator email already exists
        existing_innovator_email = db.query(InnovatorModel).filter(InnovatorModel.email == innovator_data.email).first()

        if existing_innovator_email:
            raise ValueError(f"Innovator with the email: {innovator_data.email} already exists")

        # Create nw innovator
        new_innovator = InnovatorModel(
            fullname=innovator_data.fullname,
            email=innovator_data.email,
            hashed_password=innovator_data.password,
            status=innovator_data.status,
            language=innovator_data.language,
            date_joined=datetime.now()
        )

        db.add(new_innovator)
        db.commit()
        db.refresh(new_innovator)

        logger.info(f"Created  new innovator: {new_innovator.fullname}")
        return new_innovator

    except exc.IntegrityError as e:
        logger.error(f"Database error while creating user: {str(e)}")
        db.rollback()
        raise ValueError("Error creating user. Please check your input data.")

    except Exception as e:
        logger.error(f"Unexpected error creating user: {str(e)}")
        db.rollback()
        raise

# Get a specific innovator by email
def get_innovator(email: str, db: Session, current_innovator: InnovatorModel) -> Optional[InnovatorResponse]:
    try:
        innovator = db.query(InnovatorModel).filter(InnovatorModel.email == email).first()
        if innovator:
            logger.info(f"Retrieved innovator by email: {email}")
        return innovator

    except Exception as e:
        logger.error(f"Error retrieving innovator by email {email}: {str(e)}")
        raise

# Get a list of innovators
def get_all_innovators(db: Session, current_innovator: InnovatorModel) -> List[ShowInnovator]:
    try:
        innovators = db.query(InnovatorModel).all()
        logger.info(f"Retrieved {len(innovators)}.")

    except Exception as e:
        logger.error(f"Error retrieving innovators: {str(e)}")
        raise

# Get the current innovator's information
def get_current_active_innovator(email: str, db: Session, current_innovator: InnovatorModel) -> Optional[InnovatorResponse]:
    try:
        innovator = db.query(InnovatorModel).filter(InnovatorModel.email == email).first()
        if innovator:
            logger.info(f"The current innovator goes by the name {email}.")
        return innovator

    except Exception as e:
        logger.error(f"Error retrieving current innovator by name {email}.")
        raise

# Update an existing innovator
def update_innovator(email: str, innovator_data: InnovatorUpdate, db: Session, current_innovator: InnovatorModel) -> ShowInnovator:
    try:
        existing_innovator = db.query(InnovatorModel).filter(InnovatorModel.email == email).first()
        if not existing_innovator:
            raise ValueError(f"Innovator by name {email} not found.")
        
        # Update innovator data
        existing_innovator.fullname = innovator_data.fullname
        existing_innovator.email = innovator_data.email
        existing_innovator.hashed_password = hashing.Hash.bcrypt(innovator_data.password)
        existing_innovator.status = innovator_data.status
        existing_innovator.language = innovator_data.language
        existing_innovator.updated_at = datetime.now()

        db.commit()
        db.refresh(existing_innovator)

        logger.info(f"Updated innovator: {email}.")
        return existing_innovator
    
    except exc.IntegrityError as e:
        logger.error(f"Database error updating innovator: {str(e)}.")
        db.rollback()
        raise ValueError(f"Error updating innovator. Please check if the innovator {email} exists.")
    
    except Exception as e:
        logger.error(f"Unexpected error updating innovator {email}: {str(e)}.")
        db.rollback()
        raise ValueError(f"Error updating innovator. Please check if the innovator {email} exists.")

# Delete innovator
def delete_innovator(email: str, db: Session, current_innovator: InnovatorModel) -> None:
    try:
        innovator_to_delete = db.query(InnovatorModel).filter(InnovatorModel.email == email).first()
        if not innovator_to_delete:
            raise ValueError(f"Innovator {email} not found.")

        db.delete(innovator_to_delete)
        db.commit()

        logger.info(f"Deleted innovator {email}.")

    except exc.IntegrityError as e:
        logger.error(f"Database error deleting innovator: {str(e)}.")
        db.rollback()
        raise ValueError(f"Error deleting innovator. Please check if the innovator {email} exists.")
    
    except Exception as e:
        logger.error(f"Unexpected error deleting innovator {email}: {str(e)}.")
        db.rollback()
        raise ValueError(f"Error deleting innovator. Please check if the innovator {email} exists.")