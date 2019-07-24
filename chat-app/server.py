## Webserver
from http.server import HTTPServer, BaseHTTPRequestHandler
from hashlib import sha512
from os import path, urandom
from urllib import parse
from sys import argv

OUT_IP_ADDRESS = "24.12.145.165"
INNER_IP_ADDRESS = "192.168.1.114"
PATH = path.dirname(argv[0])

ONETIMEAUTHKEY = None

with open(path.join(PATH, "chat.html"), "rb") as mfp:
    MAIN_CONTENT = mfp.read().replace(b"{ip}", OUT_IP_ADDRESS.encode())


class ServeFileOnly(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(MAIN_CONTENT)
        else:
            self.send_error(404)
            self.end_headers()
        
            
def run(server_class=HTTPServer, handler_class=ServeFileOnly):
    server_address = (INNER_IP_ADDRESS, 80)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()
