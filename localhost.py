import SimpleHTTPServer
import SocketServer

PORT = 8080

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
httpd = SocketServer.TCPServer(("", PORT), Handler)
print "listening in port: ", PORT
httpd.serve_forever()
