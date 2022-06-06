#!/bin/bash
sudo apt-get update && sudo apt-get install -y curl unzip
curl https://get.docker.com/ > get-docker.sh
chmod +x get-docker.sh
./get-docker.sh
sudo apt-get install -y docker-compose
sudo usermod -aG docker ubuntu