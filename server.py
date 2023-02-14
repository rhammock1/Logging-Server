"""
  Simple HTTP server for logging of local projets
  Author: <smokeybear> github.com/rhammock1
  Credit: <mdonkers> github.com/mdonkers for the basic web server
"""

from http.server import HTTPServer
from dotenv import load_dotenv
import logging
import json
from db import *
import LogServer

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
