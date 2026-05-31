import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.database import Base, engine

import app.model_registry

app = FastAPI(title="Cafe Finder API")

Base.metadata.create_all(bind=engine)

os.makedirs("media", exist_ok=True)

app.mount("/media", StaticFiles(directory="media"), name="media")