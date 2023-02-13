#!/bin/bash

PORT=''
if [ $1 ]; then
  PORT=$1
fi

echo "Starting server..."
python3.9 server.py $PORT
