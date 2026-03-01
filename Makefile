IMAGE_NAME := atlassian-api-mcp
CONTAINER_NAME := atlassian-api-mcp-container

.PHONY: build run run-detached stop remove logs

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the container using .env for environment variables (recommended for local testing)
run:
	docker run --rm --name $(CONTAINER_NAME) --env-file .env -p 8000:8000 $(IMAGE_NAME)

# Run the container detached (background)
run-detached:
	docker run -d --name $(CONTAINER_NAME) --env-file .env -p 8000:8000 $(IMAGE_NAME)

# Stop a running container started with the Makefile
stop:
	docker stop $(CONTAINER_NAME) || true

# Remove the container (if present)
remove:
	docker rm $(CONTAINER_NAME) || true

# Tail logs from the running container
logs:
	docker logs -f $(CONTAINER_NAME)
