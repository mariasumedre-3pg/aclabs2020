FROM python:3.7

RUN apt update
RUN apt-get install nginx -y
RUN apt-get install libmariadb-dev -y

RUN pip install Django==2.2.12
RUN pip install graphene_django==2.8.2

RUN pip install gunicorn

RUN pip install mysqlclient

COPY configuration/aclabs /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/aclabs /etc/nginx/sites-enabled

RUN mkdir /app
ADD . /app
WORKDIR /app

ENV DB_ENGINE=django.db.backends.mysql
ENV DB_NAME=aclabs2020
ENV DB_USER=admin
ENV DB_PASSWORD=rootroot
ENV DB_HOST=aclabs2020.cjnqdhi3bkuy.us-east-2.rds.amazonaws.com
ENV DB_PORT=3306

CMD [ "configuration/entrypoint.sh" ]

RUN python manage.py collectstatic --noinput