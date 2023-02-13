#!/bin/bash

if [ "$1" = "--dev" ]; then
  echo "Starting server in development mode..."
  python3.9 server.py & 

  SERVER_PROCESS_ID=$!
  echo "Server process ID: $SERVER_PROCESS_ID"

  echo "Watching server for changes..."
  echo "Press Ctrl+C to stop watching."
  # Watch the server for changes
  # while true; do
  #   # Check if a file has been saved or created in this directory


  #   echo "Restarting server..."
  #   kill $SERVER_PROCESS_ID
  #   python3.9 server.py &
  #   SERVER_PROCESS_ID=$!
else 
  echo "Starting server..."
  python3.9 server.py
fi
