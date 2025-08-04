from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.api.predict import router as predict_router
from backend.utils.preprocess import init_wav2vec  # ✅ Import model init

# ✅ Initialize FastAPI app first
app = FastAPI()

# ✅ Load Wav2Vec model once when the server starts
@app.on_event("startup")
def load_models():
    print("🚀 Initializing Wav2Vec model...")
    init_wav2vec()

# ✅ Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with actual frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Mount prediction routes
app.include_router(predict_router, prefix="/api")

# ✅ Default route
@app.get("/")
def root():
    return JSONResponse({"message": "Deepfake detection API is running."})
