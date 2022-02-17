from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class MyHandler(BaseHTTPRequestHandler):
    # HTTP Methods
    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open('my_text_file', 'rb') as html : 
            for line in html :
                self.wfile.write(line)
    def do_POST(self) :
        getattr(self, self.path[1:])(json.loads(self.rfile.read()))

try:
    pass
    server = HTTPServer(('localhost', 80), MyHandler)
    server.serve_forever()
except KeyboardInterrupt:
    server.socket.close()

print("wasda"[1:])