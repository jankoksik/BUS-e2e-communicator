FROM python:alpine

WORKDIR /python-docker
ARG OPEN_PORT
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV OPEN_PORT=${OPEN_PORT}
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE ${OPEN_PORT}

CMD python3 -m flask run --host=0.0.0.0 --port=${OPEN_PORT} 