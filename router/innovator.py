from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
import logging
from models.models import Innovator as InnovatorModel

from schema.schemas import (
    Innovator,
    InnovatorCreate,
    InnovatorUpdate,
    InnovatorResponse,
    ShowInnovator
)
from database.database import get_db
from crud.innovators import (
    create_innovator as create_innovator_crud,
    get_all_innovators as get_all_innovators_crud,
    get_innovator as get_innovator_crud,
    update_innovator as update_innovator_crud,
    delete_innovator as delete_innovator_crud,
    get_current_active_innovator as get_current_active_innovator_crud
)
from authentication.auth import (
    get_current_innovator
)

# Configure the logging with proper configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter(
    prefix="/api/innovators",
    tags=["Innovators"],
    responses={
        404: {"description": "Not found"},
        403: {"description": "Forbidden"},
        400: {"description": "Bad request"}
    }
)

# Create a new innovator
@router.post(
    "/new",
    status_code=status.HTTP_201_CREATED,
    response_model=InnovatorResponse,
    summary="Create a new innovator entry",
    description="Create a new innovator entry with the specified details",
    response_description="The created innovator entry"
)
async def create_innovator(innovator_data: InnovatorCreate, db: Session = Depends(get_db)):
    try:
        # Create an innovator
        new_innovator = create_innovator_crud(innovator_data, db)
        logger.info(f"Created new innovator: {new_innovator.fullname}")
        return new_innovator
    
    except Exception as e:
        logger.error(f"Error creating innovator: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the innovator"
        )

# Get all innovators
@router.get(
    "/all",
    response_model=List[ShowInnovator],
    summary="Get all innovators",
    description="Get a list of all innovators",
    response_description="List of innovators"
)
async def get_all_innovators(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_innovator: InnovatorModel = Depends(get_current_innovator)):
    try:
        innovators = get_all_innovators_crud(db, current_innovator)
        logger.info(f"Retrieved {len(innovators)} innovators.")
        return innovators
    except Exception as e:
        logger.error(f"Error retrieving innovators: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the innovators"
        )

# Get a specific innovator
@router.get(
    "/get-innovator",
    response_model=InnovatorResponse,
    summary="Get a specific innovator",
    description="Get a specific innovator by their fullname",
    response_description="Innovator information"
)
async def get_innovator(email: str, db: Session = Depends(get_db), current_innovator: InnovatorModel = Depends(get_current_innovator)):
    try:
        innovator = get_innovator_crud(email, db, current_innovator)
        if not innovator:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Innovator by email {email} not found"
            )
        logger.info(f"Retrieved innovator by email: {email}")
        return innovator
    except Exception as e:
        logger.error(f"Error retrieving innovator by email {email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the innovator by email"
        )

# Update an existing innovator
@router.put(
    "/update-innovator",
    response_model=InnovatorResponse,
    summary="Update an existing innovator",
    description="Update an existing innovator with the specified details",
    response_description="The updated innovator"
)
async def update_innovator(email: str, innovator_data: InnovatorUpdate, db: Session = Depends(get_db), current_innovator: InnovatorModel = Depends(get_current_innovator)):
    try:
        innovator = update_innovator_crud(email, innovator_data, db, current_innovator)
        if not innovator:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Innovator by email {email} not found"
            )
        logger.info(f"Updated innovator by email: {email}")
        return innovator
    except Exception as e:
        logger.error(f"Error updating innovator by email {email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the innovator by fullname"
        )

# Delete an innovator
@router.delete(
    "/delete-innovator",
    summary="Delete an innovator",
    description="Delete an innovator by their email",
    response_description="The deleted innovator"
)
async def delete_innovator(email: str, db: Session = Depends(get_db), current_innovator: InnovatorModel = Depends(get_current_innovator)):
    try:
        innovator = delete_innovator_crud(email, db, current_innovator)
        if not innovator:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Innovator by email {email} not found"
            )
        logger.info(f"Deleted innovator by email: {email}")
        return innovator
    except Exception as e:
        logger.error(f"Error deleting innovator by email {email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the innovator by email"
        )

# Get the current innovator's information
@router.get(
    "/current",
    response_model=InnovatorResponse,
    summary="Get the current innovator's information",
    description="Get the current innovator's information",
    response_description="The current innovator's information"
)
async def get_current_innovator(db: Session = Depends(get_db), current_innovator: InnovatorModel = Depends(get_current_innovator)):
    try:
        innovator = get_current_innovator_crud(db, current_innovator)
        if not innovator:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Current innovator not found"
            )
        logger.info(f"Retrieved current innovator: {innovator.fullname}")
        return innovator
    except Exception as e:
        logger.error(f"Error retrieving current innovator: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the current innovator"
        )

