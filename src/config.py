from pydantic_settings import BaseSettings

import os

class Settings(BaseSettings):
    app_name: str = "Glaucoma API"
    s3_dommain: str = os.environ.get('GLAUCOMA_API_S3_DOMAIN', None)
