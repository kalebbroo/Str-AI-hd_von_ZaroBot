#!/bin/bash

echo "Building Docker Image..."
docker build -t discord-strahd-bot .

echo "Running Docker Container..."
docker run discord-strahd-bot