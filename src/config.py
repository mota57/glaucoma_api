from pydantic_settings import BaseSettings

import os

class Settings(BaseSettings):
    app_name: str = "Glaucoma API"