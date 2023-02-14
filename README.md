# Python Logging Server

Simple HTTP Server for recording logs from various local projects
Uses Python3 to serve the requests and Postgresql to handle storing the logs

## Why
This server will run a Raspberry Pi and will be used for debugging
embedded projects.
This server will not run constantly, but will be started when needed

## Setup
```bash
  chmod +x setup.sh
  ./setup.sh
```

### TODO
* Add dynamic project routes
  * GET logs for project_id
* Add Queue to store logs prior to batch database insert
