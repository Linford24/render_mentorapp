from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import innovation, innovator, auth
from database.database import engine
from models import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth.router)
app.include_router(innovation.router)
app.include_router(innovator.router)
