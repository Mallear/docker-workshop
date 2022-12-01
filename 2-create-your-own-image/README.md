# Creating your own image

## Overview

In this part, we will build our own image. This way, we will be able to deploy a tagged version of our code.

## Pre requisite

- Part 0 completed

# Step 1 - Building our Nginx image

1. Configure the image

An image is the artifact used by Docker to run a container. It contains everything it needs to run. It is defined in a file named `Dockerfile` which define a list of commands to run to build the image. At the end, the image is made of multiple layers, one for each command run during the build process.

Let's look at a (really) basic Dockerfile:
```
FROM nginx:latest

COPY index.html /usr/share/nginx/html/
```

- The first line define the base image for our custom image. Here it is the latest version of the official Nginx image.
- The 2nd line execute a COPY action (copying a local file/directory to the image layer). Here we copy our index.html file to `/usr/share/nginx/html/` for Nginx to use it.

2. Build the image

Run `docker build -t nginx:custom .` while in the current directory. It will download the `nginx:latest` image if it does not find it on locally and build the image.
```
docker build -t nginx:custom .
[+] Building 0.2s (7/7) FINISHED                                                          
 => [internal] load build definition from Dockerfile                                 0.0s
 => => transferring dockerfile: 101B                                                 0.0s
 => [internal] load .dockerignore                                                    0.0s
 => => transferring context: 2B                                                      0.0s
 => [internal] load metadata for docker.io/library/nginx:latest                      0.0s
 => [internal] load build context                                                    0.0s
 => => transferring context: 643B                                                    0.0s
 => [1/2] FROM docker.io/library/nginx:latest                                        0.0s
 => [2/2] COPY index.html /usr/share/nginx/html/                                     0.0s
 => exporting to image                                                               0.0s
 => => exporting layers                                                              0.0s
 => => writing image sha256:c12fe0b66fe7722d107e11a9a1fff4cbaf3a5a44a776cd9aaf96263  0.0s
 => => naming to docker.io/library/nginx:custom                                       0.0s
```

3. Run the image

Now you can run the image with `docker run -d -p 8080:80 nginx:custom` and access it on [localhost](http://localhost:8080).

# Step 2 - More complexe images

In the `webapp/` directory is setup a python simple web app which return a basic html page. Let's look at its Dockerfile:

```
FROM python:3.9-slim-buster

WORKDIR /opt

COPY ./requirements.txt /opt/requirements.txt
COPY ./app /opt/app

RUN pip install --no-cache-dir --upgrade -r /opt/requirements.txt

ENV BACKGROUND_COLOR="blue"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

- We found the `FROM` key, to define the base image. Here we are using python 3.9, based on a slim Debian Buster image.
- `WORKDIR` key define that all command behind this line will be run from the `/opt` directory
- `COPY` key tell Docker to copy local files
- `RUN` key tell Docker to run a command, usually a bash line. Here we are using pip (python package manager) to install the app requirements
-  `ENV` key declare a default value for an environment variable. Env vars can be defined at runtime even if there are not defined inside the Dockerfile, but it helps setting a default value here.
- The `CMD` key define a list of arguments building the command the container will run once launched. Here we start a uvicorn process, which is the webserver used by this web app, with some configuration included the port on which the server should listen.

1. Build the image.

```
cd webapp/
docker build -t webapp:local .
```

2. Run the image
```
docker run -d -p 8080:80 --name webapp webapp:local
```

If you go to [localhost](http://localhost:8080/) you should see a blue web page.

3. Play with environment variable.

Stop the container: `docker stop webapp && docker rm webapp`.

Let's try to change environment variables:

```
docker run -d -p 8080:80 -e "BACKGROUND_COLOR=green" webapp:local
```
If you go to [localhost](http://localhost:8080/), this time you should see a green web page.


# Clean up

```
docker container prune
```


----

[More documentation about Docker images and Dockerfile](https://docs.docker.com/engine/reference/commandline/image/)