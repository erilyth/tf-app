# syntax=docker/dockerfile:1
   
FROM python:3.7.3-stretch
WORKDIR /flask-server
COPY . .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "server.py"]