FROM python:3.7

RUN apt-get update && apt-get install -y libmariadb-dev

RUN mkdir /app
COPY . /app
WORKDIR /app

EXPOSE 8000

RUN pwd
RUN ls
RUN pip install -r requirements.txt && \
    /app/manage.py migrate

CMD ["/app/manage.py", "runserver", "0.0.0.0:8000"]
