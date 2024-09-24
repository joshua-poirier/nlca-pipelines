# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory for the container
WORKDIR /nlca_pipelines

# System updates
RUN apt-get update && \
    apt-get install -y \
    git

# Copy virtual environment, environment variables, code into image
COPY Pipfile Pipfile.lock ./
COPY .envrc .envrc
COPY . .

# Install/update Pip and pipenv
RUN python -m pip install --upgrade pip && \
    pip install pipenv

# Install virtual environment
RUN pipenv install --system --deploy

# Specify the command to run your app
CMD python -m \
    nlca_pipelines \
    main \
    --input-filename "novi-data-engineer-assignment.csv"
