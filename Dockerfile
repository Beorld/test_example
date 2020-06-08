FROM python:3.8-slim-buster

COPY --from=docker-registry:5000/oracle-client-11.2:latest /app/oraclient /app/oraclient

WORKDIR /app

ENV ORACLE_HOME /app/oraclient
ENV LD_LIBRARY_PATH /app/oraclient/lib

COPY . .
RUN apt-get update && \
    apt-get install -y libaio1 libgeos-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Extracting drivers
RUN cd drivers && \
    tar -xzvf geckodriver.tar.gz && \
    tar -xzvf chromedriver.tar.gz && \
    cd ..
