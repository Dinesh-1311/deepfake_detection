# backend/api/predict.py
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
import os
import uuid
import shutil

from core.config import settings
from model.inference import predict_deepfake

router = APIRouter()

UPLOAD_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/predict")
async def predict(
    file: UploadFile = File(...),
    model: str = Form(...)
):
    # Save temp file
    ext = os.path.splitext(file.filename)[1]
    uid = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{uid}{ext}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run prediction
    result = predict_deepfake(file_path, model_type=model)

    # Cleanup temp file
    os.remove(file_path)

    return JSONResponse(content=result)
