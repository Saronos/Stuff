# Usamos una imagen base ligera de Python
FROM python:3.9-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos los requisitos e instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

# Exponemos el puerto 5000
EXPOSE 5000

# Comando para arrancar la app
CMD ["python", "app.py"]
