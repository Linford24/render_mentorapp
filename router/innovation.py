from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date
from models.models import (
    Innovation as InnovationModel,
    Innovator as InnovatorModel
)

from schema.schemas import (
    Innovation,
    InnovationCreate,
    InnovationUpdate,
    InnovationResponse,
    InnovationMaterial,
    Innovator,
    InnovatorCreate,
    InnovatorUpdate,
    InnovatorResponse,
    ShowInnovator
)

from database.database import get_db
from crud.innovation import (
    create_innovation as create_innovation_crud,
    get_innovation_by_name as get_innovation_by_name_crud,
    get_all_innovations_by_domain as get_all_innovations_by_domain_crud,
    get_innovators_on_innovation as get_innovators_on_innovation_crud,
    get_all_innovations as get_all_innovations_crud,
    update_innovations as update_innovations_crud,
    delete_innovation as delete_innovation_crud
)
from authentication.auth import (
    get_current_innovator
)

import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter(
    prefix="/api/innovations",
    tags=["Innovations"],
    responses={
        404: {"description": "Not found"},
        403: {"description": "Forbidden"},
        400: {"description": "Bad request"}
    }
)

# Get the General API Information
@router.get(
    "/info",
    status_code=status.HTTP_201_CREATED,
    summary="General Information about this API",
    description="This is the TransLenCe API",
    response_description="The welcome address"
)
async def info():
    return "Welcome to the world of innovations"

# Create a new innovation
@router.post(
    "/new",
    status_code=status.HTTP_201_CREATED,
    response_model=InnovationResponse,
    summary="Create a new innovation entry",
    description="Create a new innovation entry with the specified details",
    response_description="The created innovation entry"
)
async def create_innovation(innovation_data: InnovationCreate, db: Session = Depends(get_db), current_innovator: InnovatorModel = Depends(get_current_innovator)):
    try:
        # Create an innovation
        new_innovation = create_innovation_crud(innovation_data, db, current_innovator)
        logger.info(f"Created new innovation: {new_innovation.course_name}")
        return new_innovation
    
    except Exception as e:
        logger.error(f"Error creating innovation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the innovation"
        )

# Get innovation by name
@router.get(
    "/{course_name}",
    response_model=List[InnovationResponse],
    summary="Get innovation by name",
    description="Get a specific innovation by their name",
    response_description="Innovation information"
)
async def get_innovation_by_name(course_name: str, db: Session = Depends(get_db), current_innovator: InnovatorModel = Depends(get_current_innovator)):
    try:
        innovation = get_innovation_by_name_crud(course_name, db, current_innovator)
        if not innovation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Innovation by name {course_name} not found"
            )
        logger.info(f"Retrieved innovation by name: {course_name}")
        return innovation
    
    except Exception as e:
        logger.error(f"Error retrieving innovation by name: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the innovation by name"
        )

# Get all innovations by domain
@router.get(
    "/{course_domain}",
    response_model=List[InnovationResponse],
    summary="Get all innovations by domain",
    description="Get a list of all innovations under a particular domain",
    response_description="List of innovations under a particular domain"
)
async def get_all_innovations_by_domain(course_domain: str, db: Session = Depends(get_db), current_innovator: InnovatorModel = Depends(get_current_innovator)):
    try:
        innovations_by_domain = get_all_innovations_by_domain_crud(course_domain, db, current_innovator)

        if not innovations_by_domain:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Innovations under {course_domain} not found"
            )
        logger.info(f"Retrieved innovations under: {course_domain}")
        return innovations_by_domain
    
    except Exception as e:
        logger.error(f"Error retrieving innovation under {course_domain}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving the innovation under {course_domain}."
        )

# Get innovators on innovation
@router.get(
    "/{course_name}/innovators",
    response_model=List[InnovatorResponse],
    summary="Get innovators on innovation",
    description="Get a list of innovators on a particular innovation",
    response_description="List of innovators on a particular innovation"
)
async def get_innovators_on_innovation(course_name: str, db: Session = Depends(get_db), current_innovator: InnovatorModel = Depends(get_current_innovator)):
    try:
        innovators_on_innovation = get_innovators_on_innovation_crud(course_name, db, current_innovator)

        if not innovators_on_innovation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Innovators on innovation {course_name} not found"
            )
        logger.info(f"Retrieved innovators on innovation: {course_name}")
        return innovators_on_innovation
    
    except Exception as e:
        logger.error(f"Error retrieving innovators on innovation {course_name}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving the innovators on innovation {course_name}."
        )

# Get all innovations
@router.get(
    "/all",
    response_model=List[InnovationResponse],
    summary="Get all innovations",
    description="Get a list of all innovations",
    response_description="List of innovations"
)
async def get_all_innovations(db: Session = Depends(get_db), current_innovator: InnovatorModel = Depends(get_current_innovator)):
    try:
        innovations = get_all_innovations_crud(db, current_innovator)

        if not innovations:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Innovations not found"
            )
        logger.info("Retrieved all innovations")
        return innovations
    
    except Exception as e:
        logger.error(f"Error retrieving all innovations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving all innovations."
        )

# Update innovation
@router.put(
    "/update/{course_name}",
    response_model=InnovationResponse,
    summary="Update innovation",
    description="Update a specific innovation by their name",
    response_description="Updated innovation information"
)
async def update_innovation(course_name: str, innovation_data: InnovationUpdate, db: Session = Depends(get_db), current_innovator: InnovatorModel = Depends(get_current_innovator)):
    try:
        innovation = update_innovations_crud(course_name, innovation_data, db, current_innovator)

        if not innovation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Innovation by name {course_name} not found"
            )
        logger.info(f"Updated innovation by name: {course_name}")
        return innovation
    
    except Exception as e:
        logger.error(f"Error updating innovation by name {course_name}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the innovation by name {course_name}."
        )

# Delete innovation
@router.delete(
    "/delete/{course_name}",
    summary="Delete innovation",
    description="Delete a specific innovation by their name",
    response_description="Deleted innovation information"
)
async def delete_innovation(course_name: str, db: Session = Depends(get_db), current_innovator: InnovatorModel = Depends(get_current_innovator)):
    try:
        innovation = delete_innovation_crud(course_name, db, current_innovator)

        if not innovation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Innovation by name {course_name} not found"
            )
        logger.info(f"Deleted innovation by name: {course_name}")
        return innovation
    
    except Exception as e:
        logger.error(f"Error deleting innovation by name {course_name}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting the innovation by name {course_name}."
        )
