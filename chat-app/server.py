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
##    open(path.join(PATH, "admin.html"), "rb") as afp, \
##    open(path.join(PATH, "passwd.dat"), "rb") as pwdfp, \
##    open(path.join(PATH, "action.html"), "rb") as aafp:
    MAIN_CONTENT = mfp.read().replace(b"{ip}", OUT_IP_ADDRESS.encode())
##    ADMIN_CONTENT = afp.read()
##    ACTION_CONTENT = aafp.read()
##    PHASH = pwdfp.read(64)
##    SALT = pwdfp.read(128)


class ServeFileOnly(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(MAIN_CONTENT)
##        elif self.path == "/admin.html":
##            self.send_response(200)
##            self.send_header("Content-Type", "text/html")
##            self.end_headers()
##            self.wfile.write(ADMIN_CONTENT)
        else:
            self.send_error(404)
            self.end_headers()
##    def do_POST(self):
##        headers = self.headers
##        try:
##            length = int(headers["content-length"])
##        except:
##            self.send_error(411) # Length Required
##            self.end_headers()
##            return
##        data = parse.parse_qs(self.rfile.read(length))
##        if self.path == "/action-signin":
##            # Process Sign-In
##            this_phash = sha512(data[b"password"][0] + SALT).digest()
##            if this_phash == PHASH:
##               self.send_response(200) # OK Send action
##               self._auth()
##               self.end_headers()
##               self.wfile.write(ACTION_CONTENT)
##            else:
##                self.send_response(303)
##                self.send_header("Location", "/admin.html#wrong-password")
##                self.end_headers()
##        elif self.path == "/runact":
##            if data[b"action"] == "clear":
##                clear_data()
##        else:
##            self.send_error(404)
##            self.end_headers()
##    def _auth(self):
##        ONETIMEAUTHKEY = urandom(64)
##        self.send_header("Set-Cookie", "AuthToken=%s;Max-Age=300;SameSite=Strict" % ONETIMEAUTHKEY.hex())
        
            
def run(server_class=HTTPServer, handler_class=ServeFileOnly):
    server_address = (INNER_IP_ADDRESS, 80)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()
