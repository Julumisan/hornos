# Utiliza la imagen oficial de Python como base
FROM python:3.9

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requerimientos al contenedor
COPY requirements.txt .

# Instala las dependencias de tu aplicación
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente al contenedor
COPY . .

# Define el comando para ejecutar tu aplicación
CMD ["python", "menuv3.py"]