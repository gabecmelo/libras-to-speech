import http.server
import socketserver
import os
import json
import threading

class OBSServerThread(threading.Thread):
    def __init__(self, port=8080):
        super().__init__()
        self.port = port
        self.daemon = True
        self.httpd = None
        self.overlay_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'overlay')
        
        self.update_state([])

    def run(self):
        os.chdir(self.overlay_dir)
        handler = http.server.SimpleHTTPRequestHandler
        
        while True:
            try:
                self.httpd = socketserver.TCPServer(("", self.port), handler)
                print(f"OBS Overlay Server running at http://localhost:{self.port}/")
                self.httpd.serve_forever()
                break
            except OSError:
                self.port += 1

    def stop(self):
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()

    def update_state(self, history_list):
        state_path = os.path.join(self.overlay_dir, 'state.json')
        with open(state_path, 'w', encoding='utf-8') as f:
            json.dump(history_list, f, ensure_ascii=False)
