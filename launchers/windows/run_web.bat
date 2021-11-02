@echo off

CD ..
docker-compose build
docker-compose up -d
docker-compose -f docker-compose_GUI.yaml build
docker-compose -f docker-compose_GUI.yaml up -d
python -m webbrowser http:/\localhost:5000