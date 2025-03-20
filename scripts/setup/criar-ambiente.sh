#!/bin/bash

sudo docker exec -i greenbone-community-edition-gvmd-1 bash -c "mkdir auto_vas"

sudo docker exec -i greenbone-community-edition-gvmd-1 bash -c "apt-get update && apt-get install -y python3-venv python3-pip"
sudo docker exec -i greenbone-community-edition-gvmd-1 bash -c "python3 -m venv path/to/venv && \
    source /path/to/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install python-gvm gvm-tools"
sudo docker exec -i greenbone-community-edition-gvmd-1 bash -c "useradd auto_vas -s /bin/bash"