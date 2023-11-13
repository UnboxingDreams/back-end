
FROM python:3.10.10
WORKDIR /code
COPY . /code/
COPY /requirements.txt ./code/
RUN ls
RUN cd code
RUN pip uninstall pipenv
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv lock && pipenv install --dev --system --deploy
# RUN pipenv shell
# # COPY . /

# # # RUN rm Pipfile && rm Pipfile.lock
# # RUN pipenv install -r requirements.txt
# # RUN pipenv shell
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi:application"]
