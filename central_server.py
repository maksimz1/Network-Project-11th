import socket
import threading
import json
import traceback
import networking

lobbies = {}

class Lobby:
    def __init__(self, sock,lobby_id, max_players, map_name):
        self.sock = sock
        self.lobby_id = lobby_id
        self.max_players = max_players
        self.map_name = map_name

def handle_request(data, addr):
    data = json.loads(data)

    if data['request'] == '':



def handle_client(cli_sock, addr):
    print(f'New Client from {addr}')

    while True:
        try:
            data = networking.recv_by_size(cli_sock, return_type='string')
            if data == '':
                print('Seems client disconnected')
                break
            
            handle_request(data, addr)

        except socket.error as err:
            print(f'Socket Error exit client loop: err:  {err}')
            break
        except Exception as err:
            print(f'General Error %s exit client loop: {err}')
            print(traceback.format_exc())
            break

    print(f'Client Exit')
    cli_sock.close()

def main():
    threads = []

    srv_sock = socket.socket()
    srv_sock.bind(('0.0.0.0', 1233))
    srv_sock.listen()

    while True:
        cli_sock, addr = srv_sock.accept()
        t = threading.Thread(target=handle_client, args=(cli_sock, addr))
        t.start()
        threads.append(t)
