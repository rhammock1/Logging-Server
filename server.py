"""
  Simple HTTP server for logging of local projets
  Author: <smokeybear> github.com/rhammock1
  Credit: <mdonkers> github.com/mdonkers
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from dotenv import load_dotenv
import logging
import json
import psycopg2
import os

load_dotenv()

connection = None
database = None

def connect_to_db():
  try:
    connection_string = "dbname=%s user=%s" % (os.getenv("DATABASE_NAME"), os.getenv("DATABASE_USER"))
    connection = psycopg2.connect(connection_string)
    cursor = connection.cursor()
    logging.info("Connected to database...")
    return connection, cursor
  except (Exception, psycopg2.Error) as error:
    logging.error("Error while connecting to database", error)

def save_message(message, project):
  database.execute(
    """INSERT INTO messages (message, project) VALUES (%s);""",
    (message, project)
  )
  connection.commit()
  print("Records inserted successfully into messages table")

class LogServer(BaseHTTPRequestHandler):
  def _set_response(self):
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.end_headers()

  def do_GET(self):
    logging.info(
      "GET request, \nPath: %s\nHeaders:\n%s\n", 
      str(self.path), 
      str(self.headers)
    )
    self._set_response()
    self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

  def do_POST(self):
    content_length = int(self.headers['Content-Length'])
    post_data = self.rfile.read(content_length)

    body = json.loads(post_data)

    message = body["message"]
    project = body["project"]
   
    save_message(message, project)

    self._set_response()
    self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=LogServer, port=8000):
  logging.basicConfig(level=logging.INFO)
  server_address = ('', port)
  httpd = server_class(server_address, handler_class)
  try:
    logging.info("Connecting to database...")
    global connection, database
    connection, database = connect_to_db()

    logging.info("Starting HTTP server on port: %d\n", port)
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass
  logging.info('Stopping HTTP server...')
  httpd.server_close()
  logging.info('Closing database connection...')
  database.close()
  connection.close()


if __name__ == '__main__':
  from sys import argv

  if len(argv) == 2:
    run(port=int(argv[1]))
  else:
    run()
