.PHONY: build run update exec stop_container remove_container clean help

IMAGE_NAME := streamlit_testing
CONTAINER_NAME := streamlit_testing

help:
	@echo "Available rules:"
	@echo "  build            : Build the Docker image for the Streamlit application."
	@echo "  run              : Build and run the Docker container."
	@echo "  exec             : Execute a shell in the running Docker container."
	@echo "  stop_container   : Stop the running Docker container."
	@echo "  remove_container : Remove the Docker container."
	@echo "  clean            : Stop and remove the Docker container, and delete the image."

build:
	docker build -t $(IMAGE_NAME) .

run: remove_container build
	docker run -dp 8501:8501 --name $(CONTAINER_NAME) $(IMAGE_NAME)

exec:
	docker exec -it $(CONTAINER_NAME) /bin/bash

stop_container:
	docker stop $(CONTAINER_NAME) || true

remove_container: stop_container
	docker rm $(CONTAINER_NAME) || true

clean: remove_container
	docker rmi -f $(IMAGE_NAME) || true
