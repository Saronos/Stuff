import os

class Config:
    # Para desarrollo local usa SQLite (sin Docker)
    # En OpenShift usará PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///urlshortener.db'  # ← Archivo local, sin Docker
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')