FROM python:alpine

WORKDIR /python-docker
ARG OPEN_PORT
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV OPEN_PORT=${OPEN_PORT}
RUN apk add --no-cache gcc musl-dev linux-headers
RUN apk add dos2unix --update-cache --repository http://dl-3.alpinelinux.org/alpine/edge/community/ --allow-untrusted
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
EXPOSE ${OPEN_PORT}
RUN  dos2unix *.py
CMD python3 -u -m flask run --host=0.0.0.0 --port=${OPEN_PORT} 