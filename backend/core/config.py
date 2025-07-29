# OLD (remove this):
# from pydantic import BaseSettings

# NEW:
from pydantic_settings import BaseSettings  # ✅ correct import


class Settings(BaseSettings):
    upload_dir: str = "uploads"
    allowed_extensions: tuple = (".mp3", ".wav", ".mp4")

settings = Settings()
