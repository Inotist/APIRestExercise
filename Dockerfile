FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY . /app

RUN pip3 install Flask-RESTful
