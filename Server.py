import threading
import socket
import json

# Central Server for managing rooms

class Server:
    def __init__(self):
        self.rooms = {}
        self.sock = socket.socket()
        