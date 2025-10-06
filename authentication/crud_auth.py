from fastapi import status, Depends, HTTPException
from schema.schemas import Login
from sqlalchemy.orm import Session
from database import database
from models import models
from crud.hashing import pwd_ctx
from authentication import auth

async def login(credentials: Login, db: Session = Depends(database.get_db)):
    # Filter for the user whose email matches the credentials' email field
    innovator = db.query(models.Innovator).filter(models.Innovator.email == credentials.email).first()

    if not innovator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid Email: user with such email not found"
        )

    # Verification of the password 
    if not pwd_ctx.verify(credentials.password, innovator.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incorrect password"
        )

    # Generate JWT Tokens using a short-lived access token
    access_token = auth.create_access_token(data={"sub": innovator.email})

    # Create the long-lived refresh token
    refresh_token = auth.create_refresh_token(data={"sub": innovator.email})

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # For backward compatibility
    verification_token = auth.verify_token(access_token, credentials_exception, db)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "verification_token": verification_token
    }