# Use an official GDAL image as the base image
FROM osgeo/gdal:ubuntu-small-latest

# install pip
RUN apt-get update && apt-get -y install python3-pip --fix-missing

# 
WORKDIR /app/api

# 
COPY ./requirements.txt /app/api/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /app/api/requirements.txt

# 
COPY ./app /app/api/app

# 
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]