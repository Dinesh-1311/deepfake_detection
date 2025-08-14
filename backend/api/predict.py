# backend/api/predict.py
from typing import Annotated
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
from uuid import uuid4
from starlette.concurrency import run_in_threadpool

router = APIRouter()

UPLOAD_DIR = Path(__file__).resolve().parents[1] / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.get("/ping")
def ping():
    return {"api": "ok"}

@router.post("/predict")
async def predict(
    file: UploadFile = File(...),
    # ✅ default goes here, not inside Form(...)
    arch: Annotated[str, Form(alias="model_type")] = "wav2vec",
):
    # lazy import to avoid heavy startup
    from backend.model.inference import predict_deepfake

    suffix = Path(file.filename).suffix or ".wav"
    save_path = UPLOAD_DIR / f"{uuid4().hex}{suffix}"

    try:
        with save_path.open("wb") as f:
            f.write(await file.read())

        # run heavy work in threadpool
        result = await run_in_threadpool(predict_deepfake, str(save_path), arch)
        return JSONResponse(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {e}")
    finally:
        try:
            save_path.unlink(missing_ok=True)
        except:
            pass
