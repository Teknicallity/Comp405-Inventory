#!/bin/bash

SERVER_PORT="${SERVER_PORT:-8198}"

mkdir -p /etc/comp405-inventory/app/static

chown -R www-data: /etc/comp405-inventory/app/static

chown www-data: /etc/comp405-inventory

exec uwsgi --http :"$SERVER_PORT" --ini uwsgi.ini
