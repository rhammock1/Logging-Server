#!/bin/bash

# This script is used to setup a new raspberry pi with the necessary
# software to run the project. Should be run as sudo.

# Check that user is sudo
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# Update the system
echo "Updating system..."
sudo apt-get update
sudo apt-get upgrade -y

# Install postgres
echo "Installing postgres..."
sudo apt-get install postgresql -y

# Create a new user
echo "Configuring postgres..."
USER="$(whoami)"
sudo su postgres
createuser -s $USER
createdb $USER
exit

psql -c "CREATE DATABASE logging_server;"
psql -d logging_server -c "CREATE TABLE db_versions(db_version BIGSERIAL PRIMARY KEY, created TIMESTAMPTZ DEFAULT NOW());"
psql -d logging_server -c "INSERT INTO db_versions (db_version) VALUES (0);"

# Raspberry Pi should have python3.9 installed by default
# But if not, install it
echo "Installing python3.9..."
sudo apt-get install python3.9 -y

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file
echo "Creating .env file..."
echo "DATABASE_URL=postgres://$USER@localhost:5432/logging_server" >> .env

# Make serve.sh executable
echo "Making serve.sh executable..."
chmod +x ./serve.sh

echo "Setup complete. Run ./serve.sh to start the server."