from fastapi import FastAPI
from app.routers import router
from app import models, database

models.Base.metadata.create_all(bind=database.engine)


app = FastAPI()
app.include_router(router=router)