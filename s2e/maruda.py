import json
import sys
import time
import requests
import os
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket


class MarudaClub(WebSocket):
   
    def handleMessage(self):
        payload = json.loads(self.data)
        print(payload)
        client_cmd = payload['command']
        if client_cmd == 'sendmsg':
            data = {"text": payload['msg']}
            token = os.environ.get('TEAMS_TOKEN')
            response = requests.post('https://outlook.office.com/webhook/' + token, json=data)
            print(response.status_code)
        elif client_cmd == 'ready':
            pass
        else:
            print("Unknown command received", client_cmd)

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')


def run_server():
    server = SimpleWebSocketServer('', 9000, MarudaClub)
    server.serveforever()


if __name__ == "__main__":
    try:
        run_server()
    except KeyboardInterrupt:
        sys.exit(0)

