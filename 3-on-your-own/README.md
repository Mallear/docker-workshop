# On your own

In this part, you will have to write two Dockerfiles to containerize two micronaut apps and update a docker-compose configuration to run your containers.

## Pre-requisite
- Followed the [create your own image](../2-create-your-own-image/README.md) chapter
- Clone the [micronaut apps repository](https://github.com/wololock/micronaut-declarative-http-demo)

## Docker-compose

Docker compose is a tool for defining and running multi-container Docker applications. With Compose, you use a YAML file to configure your application’s services. Then, with a single command, you create and start all the services from your configuration.

Each services are defined by:
- a name
- an image
- a container name
- exposed ports
- a list of environment variables
- and a bunch more of advanced configuration

If we wanted to run the webapp from the previous labs with a docker-compose, the `docker-compose.yml` file would be:
```yml
version: '3.7' # Docker-compose version
services:
  webapp:
    image: webapp:local
    container_name: webapp
    ports:
      - '0.0.0.0:8080:80'
    environment:
      BACKGROUND_COLOR: green
```

All services defined in the same docker-compose file will share the same network by default. You can specify network configuration to avoid that, but that's a subject for later.\
In this network, services can be referenced by their name instead of their DNS, as Docker will give them random records. This means, you will be able to query services from your local network (on your laptop) using `http://localhost:8080` but containers won't be able to do that.\
If a service need access to another one, specify its host using the service name. Basically, if you have to configure a service with a reference to another service, do it this way:
```yml
services:
  datasource:
    image: datasource:<version>
    container_name: datasource

  service:
    image: service:<version>
    container_name: service
    environment:
      DB_HOST: datasource # Name of the service
```

### Docker compose usual commands

Docker compose CLI is installed with Docker Desktop.

Here are some commonly used commands:
- `docker-compose up [-d]` will trigger container creation. `-d` flag will detach the containers process from your shell (they will run in the background). If you do not use `-d` you will have live logging in your terminal.
- `docker-compose down` will stop and remove your containers
- `docker-compose stop` will stop your containers and save their states (no data loss).
- `docker-compose start` will start your stopped containers
- `docker-compose restart` will restart your containers

## Hands on

Let's use what we learned on the first labs to containerize the API and client micronaut apps of [this repository](https://github.com/wololock/micronaut-declarative-http-demo).

1. Clone the repository
2. Build the apps, starting with the API and then the client.
3. Write simple `Dockerfiles` to containerize these apps.
- Base your Dockerfiles on the `amazoncorretto:17` image
- You will want the API and client to listen to the port 80 inside the container.
- Build your image with a tag
4. Add a service to the `docker-compose.yml` file a the repository root for the API and for the client.
- Configure the API to accept traffic from your laptop on port 9090
- Configure the client to accept traffic from your laptop on port 8080
- Both API and client services should be able to reach the Consul container
- The API service should be able to reach the mariadb container
5. Start your services with `docker-compose up [-d]`. Adding `-d` will detach the process from your shell.
6. Test your apps
- Your client app should be able to accept this POST request:
```bash
curl -X POST localhost:8080/client/users -d '{"name": "JohnDoe", "email": "doe@agorapulse.com" }' -H "Content-Type: application/json"
```
- You should be able to access [`localhost:8080/client/users`](http://localhost:8080/client/users) on your laptop and get the newly create user.

**Help for advanced configuration, not covered by this workshop**:
- the API service will need mariadb container to be up and running before starting, if it's not the case it will fail at start up. A simple workaround is to add this line to the service definition: `restart: on-failure`
- A docker network is declared in the `docker-compose.yml`. For all containers to be able to reach each other, add this block to your new services configuration:
```yml
    networks:
      - demo
```

Once you've done, you can find working solutions in the [solutions](./solutions/) directory.