"""
  Simple HTTP server for logging of local projets
  Author: <smokeybear> github.com/rhammock1
  Credit: <mdonkers> github.com/mdonkers for the basic web server
"""

from http.server import HTTPServer
from dotenv import load_dotenv
import logging
import os
import ssl
from db import *
from LogServer import LogServer

load_dotenv()

def run(server_class=HTTPServer, handler_class=LogServer, use_ssl=0):
  """
  Starts the server.
  """
  logging.basicConfig(level=logging.INFO)
  port = int(os.getenv("PORT"))
  server_address = ('', port)
  httpd = server_class(server_address, handler_class)
  if use_ssl:
    print("Using SSL")
    httpd.socket = ssl.wrap_socket(
      httpd.socket,
      keyfile=os.getenv("SSL_KEY_PATH"),
      certfile=os.getenv("SSL_CERT_PATH"), server_side=True
    )
  protocol = 'HTTPS' if use_ssl else 'HTTP'
  # TODO
  # What happens if an HTTPS request is made to an HTTP server?
  try:
    logging.info("Connecting to database...")
    connect_to_db()

    logging.info("Starting %s server on port: %d\n", protocol, port)
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass
  logging.info("Stopping %s server...", protocol)
  httpd.server_close()
  logging.info('Closing database connection...')
  close_db_connection()


if __name__ == '__main__':
  from sys import argv

  if (len(argv) == 2
      and (argv[1] == "--ssl" or argv[1] == "-s")):
    run(use_ssl=1)
  else:
    run()
