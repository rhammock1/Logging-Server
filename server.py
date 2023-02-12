"""
  Simple HTTP server for logging of local projets
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

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

def run(server_class=HTTPServer, handler_class=LogServer, port=8000):
  logging.basicConfig(level=logging.INFO)
  server_address = ('', port)
  httpd = server_class(server_address, handler_class)
  logging.info("Starting HTTP server on port: %d\n", port)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass
  httpd.server_close()
  logging.info('Stopping HTTP server...\n')

if __name__ == '__main__':
  from sys import argv

  if len(argv) == 2:
    run(port=int(argv[1]))
  else:
    run()
