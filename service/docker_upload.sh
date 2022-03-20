#!/bin/sh
export DOCKER_HOST="ssh://debby@192.168.0.2"
docker-compose up -d --build --force-recreate
