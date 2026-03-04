from fastapi import FastAPI
from rooters import Classifier

app = FastAPI()

app.include_router(Classifier.router, prefix='classifier', tags=['classifier'])

@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API de NGE servant à intéragir avec Copilot"}