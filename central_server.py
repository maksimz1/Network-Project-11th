import socket
import threading
import json
import time
import traceback
import networking
import constants
import GameServer
import sys

class Lobby:
    def __init__(self, port,lobby_id, map):
        self.port = port
        self.lobby_id = lobby_id
        self.map = map
        self.players = []
        self.server = None

current_port = 1234
lck = threading.Lock()
lobbies = {}
connected_players = []
def handle_request(data, sock):
    global current_port
    global lobbies
    print(f'Handling request: {data}')
    try:
        data = json.loads(data)

        if data['request'] == 'create_lobby':
            port = current_port + 3
            current_port = port
            lobby_id = data['lobby_id']
            map = data['map']
            lobbies[lobby_id] = Lobby(port, lobby_id, map)
            lobbies[lobby_id].server = GameServer.Server(port)
            # lobbies[lobby_id] = Lobby(port, lobby_id, map)
            response = {
                'response': 'lobby_created',
                'port': port,
                'lobby_id': lobby_id,
                'map': map
            }
            networking.send_by_size(sock, json.dumps(response))
            print(f'Lobby created: {lobby_id} - {map} - {port}')

        elif data['request'] == 'join_lobby':
            lobby_id = data['lobby_id']
            if lobby_id in lobbies:
                with lck:
                    lobbies[lobby_id].players.append(sock)
                # lobbies[lobby_id].players.append(sock)
                response = {
                    'response': 'lobby_joined',
                    'port': lobbies[lobby_id].port,
                    'map': lobbies[lobby_id].map,
                    'lobby_id': lobby_id
                }
                networking.send_by_size(sock, json.dumps(response))
                print(f'Player joined lobby: {lobby_id}')

        elif data['request'] == 'lobby_list':
            with lck:
                lobby_list = [{
                    'lobby_id': lobby.lobby_id,
                    'map': lobby.map,
                    'players': len(lobby.players),
                    'port': lobby.port,
                } for lobby in lobbies.values()]
            response = {
                'response': 'lobby_list',
                'lobbies': lobby_list
            }
            networking.send_by_size(sock, json.dumps(response))
            print(f'Lobby list sent')
    except Exception as err:
        print(f'Error in handle_request: {err}')
        print(traceback.format_exc())
        sys.exit(1)

def handle_client(cli_sock, addr):
    print(f'New Client from {addr}')

    while True:
        try:
            data = networking.recv_by_size(cli_sock, return_type='string')
            if data == '':
                print('Seems client disconnected')
                break
            handle_request(data, cli_sock)

        except socket.error as err:
            print(f'Socket Error exit client loop: err:  {err}')
            break
        except Exception as err:
            print(f'General Error %s exit client loop: {err}')
            print(traceback.format_exc())
            break

    print(f'Client Exit')
    cli_sock.close()

def keep_alive():
    global connected_players
    while True:
        with lck:
            for player in connected_players:
                try:
                    request = json.dumps({"request": "keep_alive"})
                    networking.send_by_size(player, request)
                except:
                    connected_players.remove(player)
        time.sleep(constants.KEEP_ALIVE_TIME)

def main():
    threads = []

    srv_sock = socket.socket()
    srv_sock.bind(('0.0.0.0', 7878))
    srv_sock.listen()

    while True:
        cli_sock, addr = srv_sock.accept()
        t = threading.Thread(target=handle_client, args=(cli_sock, addr))
        t.start()
        threads.append(t)

if __name__ == '__main__':
    main()
