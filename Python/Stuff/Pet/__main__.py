import http.server
from Pet.Server import Handler

try:
    server = http.server.HTTPServer(('localhost', 80), Handler)
    print('Started http server')
    server.serve_forever()
except KeyboardInterrupt:
    print('^C received, shutting down server')
    server.socket.close()