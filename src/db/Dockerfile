# The new image is based on the already existing lastest mysql image.
# The mysql image can be found on https://hub.docker.com/
FROM mysql:latest

# Specifies the environment variable for the root password.
ENV MYSQL_ROOT_PASSWORD=password

# Copies the sql-scripts directory into the docker container.
# All files inside the sql-scripts directory will be executed in alphabetical order!
COPY ./sql-scripts/ /docker-entrypoint-initdb.d/

# Exposes the port 3306
# IMPORTANT! this is not the port on which you can connect to your lokal machine
EXPOSE 3306