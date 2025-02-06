IMAGE_NAME = gestor
CONTAINER_PORT = 8000
HOST_PORT = 8000
LOCAL_DIR = $(PWD)

# Start a new container
run:
	docker run -dp $(HOST_PORT):$(CONTAINER_PORT) -v $(LOCAL_DIR):/gestor $(IMAGE_NAME)

run-interactive:
	docker run -it -p $(HOST_PORT):$(CONTAINER_PORT) -v $(LOCAL_DIR):/gestor $(IMAGE_NAME) /bin/bash

# Remove all stopped containers
clean:
	docker rm $$(docker ps -a -q)

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Stop all running containers
stop:
	docker stop $$(docker ps -a -q)

# List all containers
ps:
	docker ps -a

# List all images
images:
	docker images