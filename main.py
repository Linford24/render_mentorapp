from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from router import innovation, innovator, auth
from database.database import engine
from models import models
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    models.Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: cleanup if needed


app = FastAPI(lifespan=lifespan)

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

@app.get("/")
def root():
    return {"status": "ok"}

# Mount static files directory
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve frontend.html at root path
@app.get("/home")
def landing_page():
    return FileResponse("frontend/frontend.html")

# Catalog page
@app.get("/catalog")
def catalog():
    return FileResponse("frontend/catalog.html")

# Try page
@app.get("/try")
def try_page():
    return FileResponse("frontend/try.html")



