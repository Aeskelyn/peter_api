FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN python -m venv venv
RUN pip install -r requirements.txt
RUN python manage.py migrate
RUN python manage.py createsuperuser --username Shima
COPY . /code/