FROM python:3.7
ENV PYTHONUNBUFFERED 1

# Install pipenv
RUN pip install pipenv

# Adds our application code to the image
COPY . code
WORKDIR code

# install deps from Pipfile.lock
# NOTE: remove --dev if not running locally
RUN pipenv install --dev

EXPOSE 8000

# Migrates the database, uploads staticfiles, and runs the production server
CMD pipenv run ./manage.py migrate && \
    pipenv run ./manage.py collectstatic --noinput && \
    pipenv run newrelic-admin run-program gunicorn --bind 0.0.0.0:$PORT --access-logfile - drfdemo.wsgi:application
