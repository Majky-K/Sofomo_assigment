# pull official base image
FROM python:3.10.1-slim

# set working directory
RUN mkdir -p /usr/src/api
WORKDIR /usr/src/api

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update \
    && apt-get -y install libpq-dev netcat gcc postgresql

# install python dependencies
RUN pip install --upgrade pip
#RUN pip install pipenv
#RUN pipenv install --dev
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add api
COPY . .

# add entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/api/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/usr/src/api/entrypoint.sh"]