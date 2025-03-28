#!/bin/bash

OPENVAS_DIR="/home/Auto_VAS/openvas"

cd "$OPENVAS_DIR" || { echo "Diretório não existe: $OPENVAS_DIR"; exit1; }

echo "Desligando containers do OpenVAS"
docker-compose down

echo "Fazendo download das imagens mais recentes"
docker-compose pull
docker-compose up -d

echo "Update completo!"