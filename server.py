from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import asyncio
import websockets

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
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        print('Server stopped.')


    async def handle_websocket(websocket, path):
        async for message in websocket:
            print(f"Received message: {message}")

    start_server = websockets.serve(handle_websocket, "10.3.62.240", 8000)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    run()