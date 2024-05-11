# Client to communicate with the server - Select/Create servers to join

import socket
import threading
import json
import traceback
import networking
import constants

lobbies = {}

# class Lobby:
#     def __init__(self, port, lobby_id, map):
#         self.port = port
#         self.lobby_id = lobby_id
#         self.max_players = 20
#         self.map = map
#         self.players = 0

class MenuClient:
    def __init__(self, manager):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((constants.SERVER_IP, constants.SERVER_PORT))
        self.sock.settimeout(constants.TIMEOUT_TIME)

        self.inMenu = True
        self.manager = manager 

        self.listen_thread = threading.Thread(target=self.listen)
        self.listen_thread.start()


    def listen(self):
        while self.inMenu:
            try:
                data = networking.recv_by_size(self.sock, return_type='string')
                if data == '':
                    continue

                self.handle_reply(data)
            except socket.timeout as err:
                print('Server disconnected')
                break
        
        print("Menu client stopped")
        
        # if not self.inMenu:
        #     self.sock.close()
        #     # print("Menu client stopped")
        #     return

    def handle_reply(self, data):
        data = json.loads(data)
        # print(f"Received data: {data}")

        if data['response'] == 'lobby_list':
            self.manager.lobbies = data['lobbies']
            # Beautiful print for each lobby
            # for lobby in self.manager.lobbies:
            #     print(f"Lobby ID: {lobby['lobby_id']} - Map: {lobby['map']} - Players: {lobby['players']}")


        elif data['response'] == 'lobby_created':
            # print(f"Lobby created: {data['lobby_id']} - {data['map']} - {data['port']}")
            self.get_lobby_list()

        elif data['response'] == 'lobby_joined':
            # self.manager.client.port = data['port']
            # self.manager.client.map = data['map']
            self.inMenu = False
            print("Stopping menu client")
            return
    
    def create_lobby(self, map, lobby_id):
        request = {
            'request': 'create_lobby',
            'lobby_id': lobby_id,
            'map': map
        }
        networking.send_by_size(self.sock, json.dumps(request))

    def join_lobby(self, lobby_id):
        request = {
            'request': 'join_lobby',
            'lobby_id': lobby_id
        }
        networking.send_by_size(self.sock, json.dumps(request))

    def get_lobby_list(self):
        request = {
            'request': 'lobby_list'
        }
        networking.send_by_size(self.sock, json.dumps(request))

    
        
    

