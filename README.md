# Python Logging Server

Simple HTTP Server for recording logs from various local projects
Uses Python3 to serve the requests and Postgresql to handle storing the logs

## Why
This server will run a Raspberry Pi and will be used for debugging
embedded projects.
This server will not run constantly, but will be started when needed

## Setup
* Install Python3
* Install dependencies
  * `pip install -r requirements.txt`
* Install Postgresql
* Create database
* `echo "DATABASE_URL=postgres://user:password@localhost:5432/database" >> .env`
* `chmod +x ./serve.sh`
* `./serve.sh`


### TODO
* Add dynamic project routes
  * Add projects table 
  * SELECT * FROM projects WHERE project_name = 'project_name'
  * If project exists return project_id
  * GET logs for project_id
* Read SQL files from migrations folder
* Add database migrations
* Move queries to SQL files
* Add Queue to store logs prior to batch database insert
* Add configuration script to get project started on a new machine
