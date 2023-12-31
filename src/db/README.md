## Database

In order to access the mysql and the mongodb database for this project follow the following steps, described in this readme.

### 1. Download Docker

- Download docker from the official website -> https://www.docker.com/products/docker-desktop/.
- Make sure, that docker is up and running and that it is available in your terminal/console.
  - You can test it with the `docker --help` command.

### 2. Download and build the images and containers:

- You need to be in the same directory as this readme file `src/db/`
- To automatically download the images and build the containers of both databases run `docker-compose up -d`
- To check if they are running use `docker ps`. You should see two containers up and running. Alternatively you can check the containers tab in your docker desktop.

### 3. Important `docker-compose` commands!

- If you want to build the images and run the containers use `docker-compose up -d`
- If you want to stop the containers use `docker-compose stop`. This won't delete the data inside the databases
- If you want to rerun the containers after you **stopped** them use `docker-compose start`
- If you want to stop the containers and delete them use `docker-compose down`. **CAUTION** This will also delete all your changes inside the db. But the images will not be deleted.

### 4. Information about the databases

**MySQL:**

You can use [DBeaver](https://dbeaver.io/), [MySQL Workbench](https://www.mysql.com/products/workbench/) or a [VSCode extension](https://marketplace.visualstudio.com/items?itemName=cweijan.vscode-mysql-client2)

- Connect to `localhost:3307`
- root-password: `password`
- database-name: `skillsync`

**MongoDB:**

You can either use [MongoCompass](https://www.mongodb.com/products/tools/compass) or the [VSCode extension](https://code.visualstudio.com/docs/azure/mongodb) to connect to the database

- Connect to `localhost:27017`
- root-password: `password`
- root-username: `root`
