"""
  Simple HTTP server for logging of local projets
  Author: <smokeybear> github.com/rhammock1
  Credit: <mdonkers> github.com/mdonkers for the basic web server
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from dotenv import load_dotenv
import logging
import json
from db import *

load_dotenv()

def save_message(message, project):
  try:
    result = db_file("db/messages/insert.sql", (message, project,))
    if result is None:
      logging.error("Insert message failed")
      return
    logging.info("Records inserted successfully into messages table")
  except Exception as error:
    logging.error("Error while saving message", error)


def get_messages():
  try:
    result = db_file("db/messages/get.sql")
    if result is None:
      logging.error("Get messages failed")
      return
    logging.info("Successfully retrieved messages")
    return result
  except Exception as error:
    logging.error("Error while getting message", error)

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
    messages = get_messages()

    self._set_response()
    self.wfile.write(json.dumps(messages, indent=2, default=str).encode('utf-8'))

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
    connect_to_db()

    logging.info("Starting HTTP server on port: %d\n", port)
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass
  logging.info('Stopping HTTP server...')
  httpd.server_close()
  logging.info('Closing database connection...')
  close_db_connection()


if __name__ == '__main__':
  from sys import argv

  if len(argv) == 2:
    run(port=int(argv[1]))
  else:
    run()
