FROM python:3.10.12-buster

WORKDIR /code

COPY requirements.txt /code
COPY rutorrentbot/. /code

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD [ "python", "./main.py" ]