# 321 Project Task

## Prerequisites

- Joy-Pi with installed operating system
- Docker is installed on the Joy-Pi

## Project structure

This repository contains multiple directories which hold the components of the application.

## Integral components

- `/game`: This directory holds the Python game which is being played on the Joy-Pi.
- `/dashboard`: This directory contains a web dashboard which servers as a scoreboard which displays the game score.
- `/mosquitto`: This directory contains configuration for a Mosquitto MQTT broker, which is being run by Docker.

## Non-integral components

- `/sensor-api`: This directory contains a Python application that offers an API to query the air sensor, distance sensor and the vibration unit of the Joy-Pi.
- `/sytem-monitoring`: This directory contains configuration files for monitoring utilities like Loki, Node Exporter, Prometheus, Promtail and Grafana. Those are being run by Docker.

Note that the integral components are being run by the main `docker-compose.yaml` file at the repository root. The non-integral components have their own `docker-compose.yaml` files.

## Environment Variables

Unlike the exam project, this project doesn't require you to set any environment variables.

## Running the project

To run the project, just type in the following command:

```bash
sudo docker compose up --build
```

This will build all Docker images and run the project.

**Note:** This project uses the alternative lgpio library. The `lg.zip` file contains this library. It is unzipped and installed automatically during the build process of the image.

**Note:** The application code itself isn't copied into the image itself when building the Docker image, but mounted when launching the service using the Docker Compose file.

**Note:** Make sure that the switches 4-8 on the first switch block are set to ON.

## Usage

See full documentation under `/docs`.

## LLMs / AI agents

To maximize the learning experience, I used AI to traverse documentation faster, but not to generate code automatically.

## Author

Leonardo Evic
