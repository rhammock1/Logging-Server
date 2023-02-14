from http.server import BaseHTTPRequestHandler
import logging
import json
import re
from actions.messages import save_message, get_messages


class LogServer(BaseHTTPRequestHandler):
  # Define the routes
  routes = {
      "/": {
        "method": "on_base",
        "expects": ["GET"],
      },
      "/projects": {
        "method": "on_projects",
        "expects": ["GET", "POST"],
        },
      "/projects/:project_id": {
        "method": "on_project",
        "expects": ["GET", "POST"],
        # Regex to match a number ending the path
        "regex": r"/projects/(\d+)"
        },
      "/messages": {
        "method": "on_messages",
        "expects": ["GET", "POST"],
      },
      # r"/projects/(\d+)": {
      #   "method": "on_project",
      # }
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
    print(method)
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
    # Check if the path is a dynamic route
    dynamic_routes = [key for key in self.routes if '/:' in key]
    print(dynamic_routes)
    for route in dynamic_routes:
      # Check if the path matches the regex
      if re.match(self.routes[route]['regex'], self.path):
        method_name = self.routes[route]['method']
        print(method_name)
        method = getattr(self, method_name)
        method("GET")
        return
    # check if the path is in the routes
    if self.path in self.routes:
      print(self.routes[self.path]['method'])
      method_name = self.routes[self.path]['method']
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
    # Check if the path is a dynamic route
    dynamic_routes = [key for key in self.routes if '/:' in key]
    print(dynamic_routes)
    for route in dynamic_routes:
      # Check if the path matches the regex
      if re.match(self.routes[route]['regex'], self.path):
        method_name = self.routes[route]['method']
        method = getattr(self, method_name)
        method("POST")
        return
      # exit the 
    if self.path in self.routes:
      print(self.routes[self.path])
      method_name = self.routes[self.path]['method']
      method = getattr(self, method_name)
      method("POST")
    else:
      self._set_response(404)
      self.wfile.write("Not Found".encode('utf-8'))
