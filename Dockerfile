FROM python:3.8

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /usr/src/django_movie

# install dependencies
COPY ./req.txt  /usr/src/req.txt
RUN pip install -r /usr/src/req.txt

COPY . /usr/src/django_movie

EXPOSE 8000
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]