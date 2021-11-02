#!/usr/bin/env bash

docker-compose -f "docker-compose_GUI.yaml" build
docker-compose -f "docker-compose_GUI.yaml" up -d && python -m webbrowser http://localhost:1337