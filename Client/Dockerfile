FROM python:alpine

WORKDIR /python-docker
ARG OPEN_PORT
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV OPEN_PORT=${OPEN_PORT}
RUN apk add --no-cache gcc musl-dev linux-headers
RUN apk add dos2unix --update-cache --repository http://dl-3.alpinelinux.org/alpine/edge/community/ --allow-untrusted
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE ${OPEN_PORT}
RUN  find . -name "*.py" -type f -print0 | xargs -0 -n 1 -P 4 dos2unix 

CMD python3 -u -m flask run --host=0.0.0.0 --port=${OPEN_PORT} 