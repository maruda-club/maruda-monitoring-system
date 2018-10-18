#! /usr/bin/python
# -*- coding: utf-8 -*-
#
#   server_check.py
#
#                   
# ------------------------------------------------------------------
import sys
import requests
import datetime
import json
import time
import os

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
# ------------------------------------------------------------------

class node_red():
    def get_req(self,data):
        sys.stderr.write("*** 開始 ***\n")
        #RestAPI url
        url = "http://127.0.0.1:1880/post_data"

        #TimeStamp作成
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")


        #送信データ作成
        args = {
            "YMDHMS": timestamp,
            "SENSOR_TYPE": "1",
            "SENSOR_DATA":"10"
            }

        #data['timestamp'] = timestamp
        #json 変換
        #content  = json.dumps(args)

        #payloadに送信データを入力
        #pay = {
        #    "payload": content
        #    }
        
        #REST API Get
        rr=requests.get(url,args)
        sys.stderr.write ("content = " + content + "\n")
        sys.stderr.write("*** 終了 ***\n")
        #mosquitto_sub -d -t maruda -h 10.2.192.203
    
    

class MarudaClub(WebSocket):
   
    def handleMessage(self):
        payload = json.loads(self.data)
        print(payload)
        client_cmd = payload['command']
        if client_cmd == 'sendmsg':
            data = {"text": payload['msg']}
            nrd = node_red()
            nrd.get_req(data)
            #token = os.environ.get('TEAMS_TOKEN')
            #response = requests.post('https://outlook.office.com/webhook/' + token, json=data)
            #print(response.status_code)
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
    sys.stderr.write("*** 開始 ***\n")
    server.serveforever()


if __name__ == "__main__":
    try:
        run_server()
        
    except KeyboardInterrupt:
        sys.exit(0)
        