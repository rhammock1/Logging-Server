from http.server import BaseHTTPRequestHandler
import logging
import json
from actions.messages import save_message, get_messages


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

  def on_base(self, method):
    if method == "GET":
      print("Getting Base")
      self._set_response()
      self.wfile.write("Getting Base".encode('utf-8'))
    else:
      self._set_response(404)
      self.wfile.write("Not Found".encode('utf-8'))

  def on_projects(self, method):
    if method == "GET":
      print("Getting projects")
      self._set_response()
      self.wfile.write("Getting projects".encode('utf-8'))
    elif method == "POST":
      print("Posting projects")
      self._set_response()
      self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
    else:
      self._set_response(404)
      self.wfile.write("Not Found".encode('utf-8'))

  def on_project(self, method):
    if method == "GET":
      print("Getting project")
      self._set_response()
      self.wfile.write("Getting project".encode('utf-8'))
    elif method == "POST":
      print("Posting project")
      self._set_response()
      self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
    else:
      self._set_response(404)
      self.wfile.write("Not Found".encode('utf-8'))

  def on_messages(self, method):
    if method == "GET":
      print("Getting messages")
      self._set_response()
      self.wfile.write("Getting messages".encode('utf-8'))
    elif method == "POST":
      content_length = int(self.headers['Content-Length'])
      post_data = self.rfile.read(content_length)

      body = json.loads(post_data)

      message = body["message"]
      project_id = body["project_id"]

      save_message(message, project_id)

      self._set_response()
      self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
    else:
      self._set_response(404)
      self.wfile.write("Not Found".encode('utf-8'))

  def do_GET(self):
    """
    On GET request, get all messages from the database.
    """
    # check if the path is in the routes
    if self.path in self.routes:
      method_name = self.routes[self.path]
      method = getattr(self, method_name)
      method("GET")
    else:
      self._set_response(404)
      self.wfile.write("Not Found".encode('utf-8'))

  def do_POST(self):
    """
    On POST request, get the message and project_id from the body
    and save it to the database.
    """
    if self.path in self.routes:
      method_name = self.routes[self.path]
      method = getattr(self, method_name)
      method("POST")
    else:
      self._set_response(404)
      self.wfile.write("Not Found".encode('utf-8'))
