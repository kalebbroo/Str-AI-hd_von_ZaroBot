@echo off
echo The mists are gathering...
docker build -t strahd_bot:latest .

echo Barovia is calling...
docker run --name strahd_bot strahd_bot:latest

pause