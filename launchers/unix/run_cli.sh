#!/usr/bin/env bash

docker-compose build
docker-compose up -d
clear

if [ "$(expr substr "$(uname -s)" 1 5)" == "MINGW" ]; then
  winpty docker exec -it interactive_shell fish
else
  docker exec -it interactive_shell fish
fi
