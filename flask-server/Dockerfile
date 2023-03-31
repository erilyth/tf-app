# syntax=docker/dockerfile:1
   
FROM python:3.7.3-stretch
WORKDIR /flask-server

# Install redis-tools in order to use the redis-cli for debugging purposes.
RUN apt update
RUN apt -y install redis-tools

# Copy requirements.txt first so that pip install only runs when the requirements.txt file changes and not for normal code changes.
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "server.py"]