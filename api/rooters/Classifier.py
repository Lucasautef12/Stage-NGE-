from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def classify():
    return {"message": "Cette route est destinée à classifier les documents."}



