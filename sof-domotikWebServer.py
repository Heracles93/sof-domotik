import http.server
import socketserver
from logger.logger import myLogger, sys
from logger.logger import printer as print
sys.stdout = myLogger(name = __file__.split(".")[0]+".log")

PORT = 8090
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()