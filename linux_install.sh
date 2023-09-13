#!/bin/bash

echo The mists are gathering...
docker build -t strahd_bot:latest .

echo Barovia is calling...
docker run --name strahd_bot strahd_bot:latest

# Pause the script
read -p "Press enter to continue..."