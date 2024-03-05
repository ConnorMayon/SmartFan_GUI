from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import urllib
import urllib.request
import json
import os

class CustomHandler(BaseHTTPRequestHandler):
    kivyData = {}
    #variables that are updated and sent in POST so web server can send to KIVY
    temperatures = {
        'minTempValue': 65,
        'maxTempValue': 85
    }
    time_values = {
        'hoursValue': 5,
        'tenMinutesValue': 0,
        'minutesValue': 0
    }

    def _set_headers(self, content_type='text/plain', response_type=200):
        self.send_response(response_type)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        #display main page
        if self.path == '/':
            self._set_headers(content_type='text/html')
            with open('index.html', 'rb') as f:
                html_content = f.read()
            self.wfile.write(html_content)
        if self.path == '/styles.css':
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            with open(os.path.join(os.getcwd(), 'styles.css'), 'rb') as file:
                self.wfile.write(file.read())
        #not working down to next comment
        #something like this needed for switch page on web app
        elif self.path == '/switch':
            self.send_response(301)
            self.send_header('Location', 'schedule.html')
            self.end_headers() 
            #end   
        #send kivy data to web app
        elif self.path == '/log':
            self._set_headers(content_type='application/json')
            print("KivyData:", self.kivyData)
            if CustomHandler.kivyData:
               jsonstring=json.dumps(CustomHandler.kivyData)
               self.wfile.write(jsonstring.encode('utf-8'))
            else: self.wfile.write(b'{}')
        #send web data to kivy app
        elif self.path == '/data':
            self._set_headers(content_type='application/json')
            webData={**CustomHandler.temperatures, **CustomHandler.time_values}
            print("WebData:", webData)
            if CustomHandler.kivyData:
               json_data=json.dumps(webData)
               self.wfile.write(json_data.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def do_POST(self):
        #receive Kivy Data
        if self.path == '/log':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            parsed_data = urllib.parse.parse_qs(post_data)
            minTemp=parsed_data.get('min_temp')[0]
            maxTemp=parsed_data.get('max_temp')[0]
            hourVal=parsed_data.get('hour')[0]
            tenVal=parsed_data.get('ten')[0]
            minVal=parsed_data.get('minute')[0]
            CustomHandler.kivyData=({"minTemp": minTemp, "maxTemp": maxTemp, "hourVal": hourVal, "tenVal": tenVal, "minVal": minVal})
            print(CustomHandler.kivyData)
            self._set_headers()
            self.wfile.write(b'Data received successfully')
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

        #receive Web data
        if self.path == '/update_values':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            parsed_data = json.loads(post_data)
            CustomHandler.temperatures['minTempValue'] = parsed_data['minTempValue']
            CustomHandler.temperatures['maxTempValue'] = parsed_data['maxTempValue']
            CustomHandler.time_values['hoursValue'] = parsed_data['hoursValue']
            CustomHandler.time_values['tenMinutesValue'] = parsed_data['tenMinutesValue']
            CustomHandler.time_values['minutesValue'] = parsed_data['minutesValue']
            print(CustomHandler.temperatures)
            print(CustomHandler.time_values)
            self._set_headers()
            self.wfile.write(b'Values updated successfully')
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

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

if __name__ == '__main__':
    run()