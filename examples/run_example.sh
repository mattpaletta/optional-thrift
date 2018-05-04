#!/usr/bin/env bash
docker-compose build
echo "Running in local mode"
docker-compose up client_local

echo "Running in server mode"
docker-compose up client server
