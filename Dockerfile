#Base Image from Dockerhub
FROM python:3.7

#Environment variables to be set in container

#Following env var means that python will not try to write .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
#Following env var ensures our console output looks familar and is not buffered by docker
ENV PYTHONUNBUFFERED 1

#This will be the working directory for the docker container
WORKDIR /code

#Install dependencies
#Create a Pipenv env and run Django before building the docker Image
COPY Pipfile Pipfile.lock /code/
#the "--system" command ensures that the packages we want are available in Docker
RUN pip install pipenv &&  pipenv install --system

#Get the code that will be used in the container
#WSV has Dockerfile in the Django folder and then Django Folder in a Code folder
#This somehow works
COPY . /code/
