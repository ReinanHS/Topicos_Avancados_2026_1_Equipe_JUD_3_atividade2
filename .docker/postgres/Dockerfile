FROM postgres:17

COPY init.sql /docker-entrypoint-initdb.d/01_init.sql

RUN chmod 644 /docker-entrypoint-initdb.d/01_init.sql
