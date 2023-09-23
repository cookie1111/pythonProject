FROM postgres:latest

ENV POSTGRES_PASSWORD=pass
ENV POSTGRES_USER=root
ENV POSTGRES_DB=listings

COPY init.sql /docker-entrypoint-initdb.d/

