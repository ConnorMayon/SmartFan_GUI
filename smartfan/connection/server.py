from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == '/log':
            if 'message' in query_params:
                message = query_params['message'][0]
                print("Button Pressed:", message)
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"Logged to terminal: " + message.encode())
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"Bad request: Missing 'message' parameter")
        else:
            super().do_GET()

def run():
    PORT = 8000
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, CustomHandler)
    print('Server running at port', PORT)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
