# main.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import shutil
from pathlib import Path

# ---- try to use your local modules (no 'backend.' prefix) ----
try:
    from inference import predict_deepfake  # your function (adjust if name differs)
except Exception:
    # fallback stub so the API still runs if your model code isn't ready
    def predict_deepfake(file_path: str, model_type: str) -> dict:
        # TODO: wire to your real preprocess/loader/model once ready
        return {"model": model_type, "score": 0.12, "label": "real", "extra": "stubbed result"}

app = FastAPI(title="Deepfake API", version="1.0")

# CORS so Vite (http://localhost:5173 by default) can call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # tighten to your frontend origin(s) in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/predict")
async def predict_endpoint(
    file: UploadFile = File(...),
    model_type: str = Form(default="wave2vec")  # or whatever you support
):
    # save to disk (some models need file path)
    try:
        suffix = Path(file.filename).suffix or ""
        temp_path = UPLOAD_DIR / f"input{suffix}"
        with temp_path.open("wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to save upload: {e}")

    # run inference
    try:
        result = predict_deepfake(str(temp_path), model_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {e}")

    # optionally clean up temp file
    try:
        temp_path.unlink(missing_ok=True)
    except:
        pass

    return JSONResponse(result)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
