#!/bin/bash

export SECRET_KEY=$(openssl rand -hex 20)
flask --app flaskr init-db 
sleep 3
gunicorn --bind 0.0.0.0:8000 -w 4 "flaskr:create_app()" &
sleep 5
python3 admin_read.py
