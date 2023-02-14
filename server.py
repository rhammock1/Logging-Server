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

def save_message(message, project_id):
  """
  Saves a message to the database.
  """
  try:
    result = db_file("db/messages/insert.sql", (message, project_id,))
    if result is None:
      logging.error("Insert message failed")
      return
    logging.info("Records inserted successfully into messages table")
  except Exception as error:
    logging.error("Error while saving message", error)


def get_messages():
  """
  Gets all messages from the database.
  """
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
  # Define the routes
  routes = {
    "/": "on_base",
    "/projects": "on_projects",
    "/projects/:project_id": "on_project",
    "/messages": "on_messages",
  }

  def _set_response(self, status_code=200):
    """
    Sets response status and headers
    """
    self.send_response(status_code)
    self.send_header('Content-type', 'application/json')
    self.end_headers()

  def on_base(self):
    print("Getting Base")
    self._set_response()
    self.wfile.write("Getting Base".encode('utf-8'))

  def on_projects(self):
    print("Getting projects")
    self._set_response()
    self.wfile.write("Getting projects".encode('utf-8'))

  def on_project(self):
    print("Getting project", self.path)
    self._set_response()
    self.wfile.write("Getting project".encode('utf-8'))

  def on_messages(self):
    print("Getting messages")
    self._set_response()
    self.wfile.write("Getting messages".encode('utf-8'))

  def do_GET(self):
    """
    On GET request, get all messages from the database.
    """
    logging.info(
      "GET request, \nPath: %s\nHeaders:\n%s\n", 
      str(self.path), 
      str(self.headers)
    )
    # check if the path is in the routes
    if self.path in self.routes:
      # get the method name from the routes
      method_name = self.routes[self.path]
      # get the method from 'self'.
      method = getattr(self, method_name)
      # call the method as we return it
      return method()
    else:
      self._set_response(404)
      self.wfile.write("Not Found".encode('utf-8'))

  def do_POST(self):
    """
    On POST request, get the message and project_id from the body
    and save it to the database.
    """
    content_length = int(self.headers['Content-Length'])
    post_data = self.rfile.read(content_length)

    body = json.loads(post_data)

    message = body["message"]
    project_id = body["project_id"]
   
    save_message(message, project_id)

    self._set_response()
    self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=LogServer, port=8000):
  """
  Starts the server.
  """
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
