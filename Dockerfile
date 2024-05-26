FROM python:3.10.12-buster

WORKDIR /code

COPY requirements.txt /code
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY rutorrentbot/. /code

CMD [ "python", "./main.py" ]