FROM ubuntu:latest
LABEL authors="vy"

RUN apt update && apt upgrade -y && apt install -y python3 pip
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
COPY . /opt

ENTRYPOINT ["python3", "/opt/main.py"]