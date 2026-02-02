FROM python:3.9-slim

WORKDIR /app

# Esto copia TODO tu código al contenedor
COPY . .

RUN pip install -r requirements.txt

# SI TU ARCHIVO ESTÁ EN LA RAÍZ:
CMD ["python", "app.py"]

# SI TU ARCHIVO ESTÁ DENTRO DE UNA CARPETA 'src':
# CMD ["python", "src/app.py"]