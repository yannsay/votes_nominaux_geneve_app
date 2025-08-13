FROM python:3.13.5-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /votes_nominaux_geneve_app
WORKDIR /votes_nominaux_geneve_app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["sh", "-c", "python etl_votes_nominaux_geneve/etl_votes_nominaux_geneve.py && python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8080"]
