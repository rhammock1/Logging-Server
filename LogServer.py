from http.server import BaseHTTPRequestHandler
import logging
import json
import re
from actions.messages import save_message, get_messages
from actions.projects import save_project, get_projects, get_project


class LogServer(BaseHTTPRequestHandler):
  # Define the routes
  routes = {
    r"/$": {
        "method": "on_base",
        "expects": ["GET"],
    },
    r"/messages$": {
      "method": "on_messages",
      "expects": ["GET", "POST"],
    },
    r"/projects$": {
      "method": "on_projects",
      "expects": ["GET", "POST"],
    },
    r"/projects/(\d+)$": {
      "method": "on_project",
      "expects": ["GET", "POST"],
    }
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
  
  def get_route(self, method):
    """
    Gets the route from the routes dictionary and calls the method.
    Returns True if the route is found, False otherwise.
    """
    matched = False
    for key in self.routes.keys():
      print(key)
      if re.match(key, self.path):
        method_name = self.routes[key]['method']
        print(method_name)
        method = getattr(self, method_name)
        method("POST")
        matched = True
        break
    return matched

  def do_GET(self):
    matched = self.get_route('GET')
    if not matched:
      self._set_response(404)
      self.wfile.write("Not Found".encode('utf-8'))

  def do_POST(self):
    matched = self.get_route('POST')
    
    if not matched:
      self._set_response(404)
      self.wfile.write("Not Found".encode('utf-8'))
