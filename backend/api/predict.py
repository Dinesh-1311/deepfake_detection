import os
from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse

from backend.model.inference import predict_deepfake

router = APIRouter()

@router.post("/predict")
async def predict(file: UploadFile = File(...), model_type: str = Form(...)):
    try:
        contents = await file.read()
        os.makedirs("uploads", exist_ok=True)  # ✅ Ensure 'uploads/' exists
        file_id = uuid4().hex
        save_path = f"uploads/{file_id}_{file.filename}"

        with open(save_path, "wb") as f:
            f.write(contents)

        result = predict_deepfake(save_path, model_type)
        return result

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
