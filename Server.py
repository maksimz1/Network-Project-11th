import socket
import threading
import json

HOST_IP = '0.0.0.0'
HOST_UDP_PORT = 7878

class Player():
	def __init__(self, id, pos, rot, address):
		self.id = id
		self.pos = pos
		self.rot = rot
		self.address = address
		self.weapon = None

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
			print(f"Player {new_player_id} connected from {addr}")

			request = json.dumps(
				{
					"request": "hello_accept",
				    "player_id": new_player_id
				 }
			)
			self.sock.sendto(request.encode(), addr)

			self.broadcast_player_connection(self.connected_players[new_player_id])

			# Send the data of all the connected players to the new player
			self.send_player_list(addr)


		elif data['request'] == 'update_location':
			player_id = data['player_id']
			player_pos = data['player_pos']
			player_rot = data['player_rotation']
			player_state = data['player_state']
			self.connected_players[player_id].pos = player_pos
			self.connected_players[player_id].rot = player_rot
			self.connected_players[player_id].state = player_state
			self.broadcast_player_location(self.connected_players[player_id])

		elif data['request'] == 'disconnect':
			player_id = data['player_id']
			del self.connected_players[player_id]
			print(f"Player {player_id} disconnected")
			self.broadcast_player_disconnect(player_id)
		
		elif data['request'] == 'switch_weapon':
			player_id = data['player_id']
			weapon_type = data['weapon_type']
			self.connected_players[player_id].weapon = weapon_type
			print(f"Player {player_id} switched to weapon {weapon_type}")
			self.broadcast_weapon_switch(player_id, weapon_type)
			
	def broadcast_player_connection(self, data: Player):
		request = json.dumps(
			{
				"request": "new_player",
				"player_id": data.id,
				"player_pos": data.pos,
				"player_rotation": data.rot
			}
		)
		for player in self.connected_players.values():
			self.sock.sendto(request.encode(), player.address)
		
	def broadcast_player_disconnect(self, player_id):
		request = json.dumps(
			{
				"request": "player_disconnect",
				"player_id": player_id
			}
		)

		for player in self.connected_players.values():
			if player.id == player_id:
				continue
			self.sock.sendto(request.encode(), player.address)

	def broadcast_player_location(self, data: Player):

		request = json.dumps(
			{
				"request": "update_player_location",
				"player_id": data.id,
				"player_pos": data.pos,
				"player_rotation": data.rot,
				"player_state": data.state

			}
		)

		for player in self.connected_players.values():
			self.sock.sendto(request.encode(), player.address)
	
	def broadcast_weapon_switch(self, player_id, weapon_type):
		request = json.dumps(
			{
				"request": "switch_weapon",
				"player_id": player_id,
				"weapon": weapon_type
			}
		)

		for player in self.connected_players.values():
			if player.id == player_id:
				continue
			self.sock.sendto(request.encode(), player.address)

	def send_player_list(self, addr):
		request = {"request": "players_list", "players": []}
		for player in self.connected_players.values():
			request["players"].append(
				{
					"player_id": player.id,
					"player_pos": player.pos,
					"player_rotation": player.rot
				}
			)
		request = json.dumps(request)
		
	def generate_player_id(self):
		# Generate a new player id
		# Account for the fact that players can leave
		# and the id can be reused
		new_player_id = 0
		while new_player_id in self.connected_players:
			new_player_id += 1
		return new_player_id

	def get_player_by_address(self, addr):
		for player in self.connected_players.values():
			if player.address == addr:
				return player
		return None

	def communication_handle(self):
		while True:
			# Recieve data using recv_by_size
			try:
				data, addr = self.sock.recvfrom(65535)
			except ConnectionResetError:
				# print("Prloblem")
				continue
			if data:
				# Handle the request
				self.handle_request(data, addr)




def main():
	server = Server()
	server.communication_handle()
	
if __name__ == '__main__':
	main()
