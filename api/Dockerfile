# Use an official GDAL image as the base image
FROM ghcr.io/osgeo/gdal:ubuntu-small-3.10.0

# install pip
RUN apt-get update && apt-get -y install python3-pip --fix-missing

# 
WORKDIR /app/api

# 
COPY ./requirements.txt /app/api/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade --break-system-packages -r /app/api/requirements.txt

# 
COPY ./app /app/api/app

# 
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]