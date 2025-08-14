# backend/main.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool
from pathlib import Path
import shutil
import uvicorn
from uuid import uuid4
from backend.api.predict import router as predict_router


app = FastAPI(title="Deepfake API (testing)", version="1.0")

# CORS for quick testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_router, prefix="/api") 

@app.get("/health")
def health():
    return {"ok": True}

UPLOAD_DIR = (Path(__file__).resolve().parent / "uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/predict")
async def predict_endpoint(
    file: UploadFile = File(...),
    arch: str = Form(default="wav2vec"),   # default so you don't need to send model_type
):
    # ✅ lazy import so startup stays instant
    from backend.model.inference import predict_deepfake

    # save upload
    suffix = Path(file.filename).suffix or ".wav"
    tmp_path = UPLOAD_DIR / f"{uuid4().hex}{suffix}"
    try:
        with tmp_path.open("wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to save upload: {e}")

    # run heavy compute off the event-loop
    try:
        result = await run_in_threadpool(predict_deepfake, str(tmp_path), arch)
        return JSONResponse(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {e}")
    finally:
        try:
            tmp_path.unlink(missing_ok=True)
        except:
            pass

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
