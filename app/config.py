import os


class Config:
    # Local: SQLite (sin instalaciones extra)
    # OpenShift: PostgreSQL (configurado por variable de entorno)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///urlshortener.db'  # Base de datos local en un archivo
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')
