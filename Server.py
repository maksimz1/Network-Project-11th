import socket
import threading
import json

HOST_IP = '0.0.0.0'
HOST_UDP_PORT = 7895

class Player():
	def __init__(self, id, pos, rot, address):
		self.id = id
		self.pos = pos
		self.rot = rot
		self.address = address
class Server():
	def __init__(self):
		# Initialize game environment
		# connected_players - dictionary to store the data of each player alongside their address
		self.connected_players = {}

		# Initialize the socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind((HOST_IP, HOST_UDP_PORT))
		print("Server started")

	def handle_request(self, data, addr):
		# print(f"Recieved data from {addr}")
		# print(data)

		data = data.decode()
		data = json.loads(data)
		if data['request'] == 'hello':
			new_player_id = self.generate_player_id()
			player_pos = data['player_pos']
			player_rot = data['player_rotation']
			self.connected_players[new_player_id] = (Player(new_player_id, player_pos, player_rot, addr))
			print(f"Player {new_player_id} connected")

			request = json.dumps(
				{
					"request": "hello_accept",
				    "player_id": new_player_id
				 }
			)
			self.sock.sendto(request.encode(), addr)

			self.broadcast_player_connection(self.connected_players[new_player_id])


		elif data['request'] == 'update_location':
			player_id = data['player_id']
			player_pos = data['player_pos']
			player_rot = data['player_rotation']
			self.connected_players[player_id].pos = player_pos
			self.connected_players[player_id].rot = player_rot
			self.broadcast_player_location(self.connected_players[player_id])



	def broadcast_player_connection(self, data: Player):
		request = json.dumps(
			{
				"request": "new_player",
				"player_id": data.id,
				"player_pos": data.pos,
				"player_rotation": data.rot
			}
		)
		print(f"Broadcasting new player {data.id}")
		for player in self.connected_players.values():
			self.sock.sendto(request.encode(), player.address)

	def broadcast_player_location(self, data: Player):

		request = json.dumps(
			{
				"request": "update_player_location",
				"player_id": data.id,
				"player_pos": data.pos,
				"player_rotation": data.rot
			}
		)

		for player in self.connected_players.values():
			print(f"Broadcasting player {data.id} location to player {player.id}")
			self.sock.sendto(request.encode(), player.address)

	def generate_player_id(self):
		new_player_id = len(self.connected_players)
		return new_player_id

	def communication_handle(self):
		while True:
			# Recieve data using recv_by_size
			try:
				data, addr = self.sock.recvfrom(65535)
			except ConnectionResetError:
				print("Connection reset by peer")
				continue
			if data:
				# Handle the request
				self.handle_request(data, addr)





server = Server()
server.communication_handle()
