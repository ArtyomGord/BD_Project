FROM postgres:latest

LABEL author="ArtyomGord"
LABEL description="Transport System Database"
LABEL version="1.0"

COPY *.sql /docker-entrypoint-initdb.d/