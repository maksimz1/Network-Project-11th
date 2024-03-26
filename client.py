from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import socket
import threading
import json

app = Ursina(borderless=False, fullscreen=False, window_title='Client')

SERVER_IP = '127.0.0.1'
SERVER_UDP_PORT = 7895

PLAYER_SCALE = (1, 2.5, 1)
Y_OFFSET = 0.5 * PLAYER_SCALE[1] - 0.1


class Player(Entity):
	def __init__(self):
		super().__init__()
		self.speed = 2.5
		self.jump_height = 0.5
		self.gravity = 0.5
		self.jumping = False
		self.player_id = None
		self.controller = FirstPersonController()
		self.prev_location = self.controller.position
		self.prev_rotation = self.controller.rotation

		self.create_ground()
		self.create_connection()

		self.connected_players = {}

	def create_connection(self):

		# Create a UDP socket and connect to the server
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.connect((SERVER_IP, SERVER_UDP_PORT))
		self.send_hello()
		# Save the player's ID
		while self.player_id is None:
			data = self.sock.recv(65535)
			if data:
				data = json.loads(data.decode())
				self.player_id = data['player_id']

	def create_ground(self):
		# ground = Entity(model=r'Assets\ground.obj', texture=r'Assets\Grass.jpg', scale=(1, 1, 1), position=(0, -5, 0),
		#                 collider='mesh')
		ground = Entity(model='plane', texture='grass', scale=(100, 100, 100), position=(0, -5, 0), collider='box')

	def change_fov(self, fov):
		camera.fov = lerp(camera.fov, fov, 8 * time.dt)

	# Send the player's location to the server
	def send_location_update(self):
		player_pos = self.controller.position
		player_rot = self.controller.rotation

		request = json.dumps(
			{
				"request": "update_location",
				"player_id": self.player_id,
				"player_pos": [player_pos.x, player_pos.y, player_pos.z],
				"player_rotation": [player_rot.x, player_rot.y, player_rot.z]
			}
		)

		self.sock.sendall(request.encode())

	def send_hello(self):
		player_pos = self.controller.position
		player_rot = self.controller.rotation

		request = json.dumps(
			{
				"request": "hello",
				"player_pos": [player_pos.x, player_pos.y, player_pos.z],
				"player_rotation": [player_rot.x, player_rot.y, player_rot.z]
			}
		)
		self.sock.sendall(request.encode())

	def build_request(self, request_type):
		if request_type == "hello":
			player_pos = self.controller.position
			player_rot = self.controller.rotation

			request = json.dumps(
				{
					"request": "hello",
					"player_pos": [player_pos.x, player_pos.y, player_pos.z],
					"player_rotation": [player_rot.x, player_rot.y, player_rot.z]
				}
			)
		elif request_type == "update_location":
			player_pos = self.position
			# player_pos = self.controller.position
			player_rot = self.controller.rotation

			request = json.dumps(
				{
					"request": "update_location",
					"player_pos": [player_pos.x, player_pos.y, player_pos.z],
					"player_rotation": [player_rot.x, player_rot.y, player_rot.z]
				}
			)
		return request

	def update(self):

		# Check if the player has moved
		if self.prev_location != self.controller.position or self.prev_rotation != self.controller.rotation:
			# Send the player's location to the server
			self.send_location_update()

		if held_keys['shift']:
			# Increase the player speed and fov
			self.change_fov(110)
			self.controller.speed = 10
		else:
			# Reset the player speed and fov
			self.change_fov(80)
			self.controller.speed = 5

		self.prev_location = self.controller.position
		self.prev_rotation = self.controller.rotation


class Client():
	def __init__(self):
		self.player = Player()

		sky = Sky()

		listen_thread = threading.Thread(target=self.listen)
		listen_thread.start()

	def listen(self):
		while True:
			data, addr = self.player.sock.recvfrom(65535)
			if addr == (SERVER_IP, SERVER_UDP_PORT) and data:
				self.handle_request(data)

	def add_player(self, player_id, player_pos, player_rotation):
		adjusted_position = (player_pos[0], player_pos[1] + Y_OFFSET, player_pos[2])
		self.player.connected_players[player_id] = Entity(model='cube', collider='box', texture=r'Assets\bengvir.jpg',
		                                                  position=adjusted_position, rotation=player_rotation,
		                                                  scale=PLAYER_SCALE)

	def handle_request(self, data):
		data = json.loads(data.decode())
		if data['request'] == 'hello_accept':
			self.player.player_id = data['player_id']
			print(f"Player {self.player.player_id} connected")
		elif data['request'] == 'new_player':

			if data['player_id'] == self.player.player_id:
				return
			print(f"New player connected {data['player_id']}")
			player_id = data['player_id']

			adjusted_position = (data['player_pos'][0], data['player_pos'][1] + Y_OFFSET, data['player_pos'][2])

			self.add_player(player_id, data['player_pos'], data['player_rotation'])

			print(f"Player {player_id} connected")

		elif data['request'] == 'update_player_location':

			adjusted_position = (data['player_pos'][0], data['player_pos'][1] + Y_OFFSET, data['player_pos'][2])
			if data['player_id'] == self.player.player_id:
				return
			elif data['player_id'] not in self.player.connected_players:
				self.add_player(data['player_id'], data['player_pos'], data['player_rotation'])

			player_id = data['player_id']
			self.player.connected_players[player_id].position = adjusted_position
			self.player.connected_players[player_id].rotation = data['player_rotation']


client = Client()
app.run()
