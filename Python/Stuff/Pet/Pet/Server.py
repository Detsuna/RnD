
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from os import path
import sqlite3 as sql

PORT = 80

class Handler(BaseHTTPRequestHandler) : 
    def __init__(self, *a, **k) : 
        self.db = sql.connect(path.join(path.dirname(path.realpath(__file__)), 'src.db'))
        self.db.row_factory = sql.Row
        super().__init__(*a, **k)
    def do_GET(self):
        print(self.path)
        try : 
            cur = self.db.cursor()
            row = cur.execute("SELECT * FROM [Files] WHERE [Path]=@Path", {"Path": self.path}).fetchone()
            if row is None : raise
            
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", row["Type"])
            self.end_headers()
            self.wfile.write(row["Content"])
            
        except :
            self.send_response(HTTPStatus.NOT_FOUND)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><head><title>Title goes here.</title></head>")
            self.wfile.write(b"<body><p>This is a test.</p>")
            self.wfile.write(b"</body></html>")