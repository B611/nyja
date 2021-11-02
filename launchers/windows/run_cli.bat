@echo off

CD ..
docker-compose build
docker-compose up -d
docker exec -it interactive_shell fish