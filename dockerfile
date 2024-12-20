# Obtener imagen base
FROM python:3.10.4-slim-bullseye

# Configurar variables de entorno
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar netcat para wait-for-it
RUN apt-get update && apt-get install -y netcat

# Configurar directorio de trabajo
WORKDIR /app

# Copiar los requisitos y luego instalar dependencias
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Exponer el puerto 8000
EXPOSE 8000

