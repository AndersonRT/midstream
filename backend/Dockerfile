FROM python:3.7.3

RUN mkdir -p /home/project/backend
WORKDIR /home/project/backend
COPY requirements.txt /home/project/backend
COPY pkgs /home/project/backend/pkgs
RUN pip install --no-cache-dir -r requirements.txt

COPY . /home/project/backend

