# Dockerfile

# Pull base image
FROM python:3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
RUN mkdir /code
WORKDIR /code

RUN pip install virtualenv
CMD . venv/bin/activate

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy project
COPY . /code/
