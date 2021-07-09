#FROM python:3
FROM tiangolo/uwsgi-nginx-flask:python3.8

#WORKDIR /usr/src/app
RUN apt update
RUN apt-get install ffmpeg libsm6 libxext6  -y
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

#COPY . .
COPY . /app

#ENTRYPOINT [ "python", "/usr/src/app/web.py"  ]