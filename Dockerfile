
FROM python:3.10.10
COPY /app/requirements.txt ./
RUN pipenv install -r requirements.txt
EXPOSE 8000
RUN python manage.py runserver 0.0.0.0:8000