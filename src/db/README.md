## Database

In order to access the mysql database for this project follow the following steps, described in this readme.

### 1. Download Docker

- Download docker from the official website -> https://www.docker.com/products/docker-desktop/.
- Make sure, that docker is up and running and that it is available in your terminal/console.
  - You can test it with the `docker --help` command.

### 2. Build the image inside the current directory:

Docker containers are build with docker images, so first of all we need to build our docker image with our Dockerfile:

- Navigate into the directory "src/db"
- Build the image with:
  - `docker build -t database-image .`
    - `-t` specifies a tag/name for the image, which is to be build
    - `.` specifies that the image should be build based on the Dockerfile of the current directory

### 3. Run the container, from the image:

After "building" the image you can "run" the container. After running the container the database can be accessed.

- To tun the container use:
  - `docker run --name database-container -p 3307:3306 -d database-image`
    - `--name` refers to the name of the container, which can be set with this flag.
    - `-p` refers to the port, where the database should run on.
      - 3306 is the port which is exposed by the container
      - 3307 is the port on your local machine, on which you can connect to the database.
    - `-d` refers to "detached mode", which means there will be no logs in the current terminal window. If you want to see the logs of the db you can remove this flag.

# Important

- Once the container is build you can stop and restart it.
- **You don't need to rebuild the container**. In case you need/want to rebuild the container, all the data you added or changed in the db is lost!!!
- To stop a container use:
  - `docker stop <container-name>`
- To start/restart a container use:
  - `docker start <container-name>`
