#https://hub.docker.com/_/postgres

FROM postgres:15.1

CMD ["mkdir", "./docker-entrypoint-initdb.d"]
COPY ./TestDB.sql ./docker-entrypoint-initdb.d
