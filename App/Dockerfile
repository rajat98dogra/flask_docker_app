FROM python:3.6

ADD . /home
WORKDIR /home

RUN pip install -r requirements.txt
CMD uwsgi app.ini