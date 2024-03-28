from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import socket
import threading
import json
from ursina import Entity
from direct.actor.Actor import Actor
import random

app = Ursina(borderless=False, fullscreen=False, window_title='Client')

SERVER_IP = '127.0.0.1'
SERVER_UDP_PORT = 7878

WEAPONS_FILE = 'Weapons.json'
PLAYER_SCALE = (1,1,1)
lock = threading.Lock()

# Class for the player's weapon
class Weapon(Entity):
	def __init__(self, camera_pivot, damage, fire_rate, ammo, magazine_size ,weapon_type ,position = (0,0,0), rotation = (0,0,0), scale = (0.4, 0.4, 0.4)):
		super().__init__()
		# Initialize the weapon's model, texture, and position in the player's hand
		self.parent = camera_pivot
		self.weapon_type = weapon_type
		self.position = Vec3(0.6, -0.5, 1) + position
		self.scale = scale
		self.rotation = Vec3(0, 90, 0)+ rotation
		self.damage = damage
		self.fire_rate = fire_rate
		self.ammo = ammo
		self.magazine_size = magazine_size
		self.current_ammo = self.magazine_size
		self.on_cooldown = False
		self.enabled = False

	# Function to shoot the weapon
	def shoot(self):
		if not self.on_cooldown:
			has_hit = self.check_hit()
			
			self.on_cooldown = True

			invoke(setattr, self, 'on_cooldown', False, delay=0.2/self.fire_rate)
			from ursina.prefabs.ursfx import ursfx
			ursfx([(0.0, 0.0), (0.1, 0.9), (0.15, 0.75), (0.3, 0.14), (0.6, 0.0)], volume=0.5, wave='noise', pitch=random.uniform(-13,-12), pitch_change=-12, speed=3.0)
	
	def check_hit(self):
		# Get direction of crosshair
		shoot_direction = camera.forward
		# Check if the weapon hit any player
		# print(f"Shooting {self.weapon_type}")
		# print(f"Camera position: {camera.position}")
		# print(f"Camera position word: {camera.world_position}")
		hit_info = raycast(camera.world_position, shoot_direction, distance=100, ignore=[self, camera],debug=True )		
		if hit_info.hit:
			# print(f"Hit {hit_info.entity.name} for {self.damage} damage")
			print(f"Hit {hit_info.entity} for {self.damage} damage")
		
	

class Pistol(Weapon):
	def __init__(self, camera_pivot, position = (0,0,0), rotation = (0,0,0), scale = (0.3, 0.3, 0.3)):
		super().__init__(camera_pivot, damage=10, fire_rate=0.4, ammo=60, magazine_size=15, weapon_type="Pistol", position=position, rotation=rotation, scale=scale)
		self.model = 'Assets/Models/Pistol.obj'



class Player(Entity):
	def __init__(self):
		super().__init__()
		
		self.jumping = False
		self.player_id = None
		self.controller = FirstPersonController()

		self.prev_location = self.controller.position
		self.prev_rotation = self.controller.rotation
		self.state = "idle"
		self.prev_state = "idle"
		self.health = 100

		self.weapon_inventory = [Pistol(self.controller.camera_pivot)]
		self.current_weapon = None
	
		self.create_ground()
		self.create_connection()

		
		self.game_running = True
		
		self.connected_players = {}

	def create_connection(self):

		# Create a UDP socket and connect to the server
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.settimeout(0.01)
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

	def check_state(self):
		self.prev_state = self.state
		if self.controller.position != self.prev_location:
			self.state = "moving"
		else:
			self.state = "idle"
	
	def equip_weapon(self, index=0):
		# If the player has the weapon equipped, unequip it
		if self.current_weapon == self.weapon_inventory[index]:
			self.current_weapon.enabled = False
			self.current_weapon = None

		# If the player has another weapon equipped, unequip it and equip the new weapon
		elif self.current_weapon is not None:
			self.current_weapon.enabled = False
			self.current_weapon = self.weapon_inventory[index]
			self.current_weapon.enabled = True

		# Equip the weapon
		elif self.weapon_inventory[index] is not None:
			self.current_weapon = self.weapon_inventory[index]
			self.current_weapon.enabled = True

		else:
			return None
		
		# Send weapon switch update to server
		self.send_weapon_switch()


	def send_weapon_switch(self):
		request = self.build_request("switch_weapon")
		self.sock.sendall(request.encode())

	# Send the player's location to the server
	def send_location_update(self):
		player_pos = self.controller.position
		player_rot = self.controller.rotation

		# Check player state
		
		request = json.dumps(
			{
				"request": "update_location",
				"player_id": self.player_id,
				"player_pos": [player_pos.x, player_pos.y, player_pos.z],
				"player_rotation": [player_rot.x, player_rot.y, player_rot.z],
				"player_state": self.state
			}
		)

		self.sock.sendall(request.encode())

	def send_hello(self):
		hello_request = self.build_request("hello")
		self.sock.sendall(hello_request.encode())
	

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
			player_pos = self.controller.position
			# player_pos = self.controller.position
			player_rot = self.rotation

			request = json.dumps(
				{
					"request": "update_location",
					"player_pos": [player_pos.x, player_pos.y, player_pos.z],
					"player_rotation": [player_rot.x, player_rot.y, player_rot.z]
				}
			)
		
		elif request_type == "disconnect":
			request = json.dumps(
				{
					"request": "disconnect",
					"player_id": self.player_id
				}
			)
		elif request_type == "switch_weapon":
			request = json.dumps(
				{
					"request": "switch_weapon",
					"player_id": self.player_id,
					"weapon_type": self.current_weapon.weapon_type if self.current_weapon is not None else None
				}
			)
		return request
	
	def input(self, key):
		if key == 'escape':
			with lock:
				self.game_running = False
				request = self.build_request("disconnect")
				print("Disconnecting")
				self.sock.sendall(request.encode())
			quit()
		if key == 'r':
			self.equip_weapon()
		if key == 'left mouse down':
			if self.current_weapon is not None:
				self.current_weapon.shoot()
			
		
	def update(self):
		
		self.check_state()

		if self.state == "moving" or self.state != self.prev_state or self.controller.rotation != self.prev_rotation:
			# Send the player's location to the server
			self.send_location_update()

		if held_keys['shift']:
			# Increase the player speed and fov
			self.change_fov(90)
			self.controller.speed = 10
		else:
			# Reset the player speed and fov
			self.change_fov(80)
			self.controller.speed = 5

		

		self.prev_location = self.controller.position
		self.prev_rotation = self.controller.rotation

class OtherPlayer(Entity):
	def __init__(self, player_id, player_pos, player_rotation, player_model):
		super().__init__()
		self.player_id = player_id
		self.position = player_pos
		self.rotation = player_rotation
		self.model = player_model
		self.collider = 'mesh'
		self.scale = PLAYER_SCALE
		self.name = "Player " + str(player_id)

		self.weapons_inventory = {"Pistol": Pistol(self, scale=(1,1,1), position=(0.3,1,0), rotation=(0,0,0))}
		self.current_weapon = None
		self.enabled = True

class Client():
	def __init__(self):
		self.player = Player()

		sky = Sky()

		listen_thread = threading.Thread(target=self.listen)
		listen_thread.start()
	
	def listen(self):
		while True:
			with lock:
				if not self.player.game_running:
					self.player.sock.close()
					break
				else:
					try:
						data, addr = self.player.sock.recvfrom(65535)
						if addr == (SERVER_IP, SERVER_UDP_PORT) and data:
							self.handle_request(data)
					except socket.timeout:
						pass
	
	def add_player(self, player_id, player_pos, player_rotation):
		chicken_model = load_model(r'Assets\Models\Chicken.obj')
		self.player.connected_players[player_id] = OtherPlayer(player_id, player_pos, player_rotation, chicken_model)
	

	def handle_request(self, data):
		data = json.loads(data.decode())
		if data['request'] == 'hello_accept':
			self.player.player_id = data['player_id']

			print(f"Player {self.player.player_id} connected")

		elif data['request'] == 'new_player':

			if data['player_id'] == self.player.player_id:
				return
			print(f"New player connected {data['player_id']}")
			self.add_player(data['player_id'], data['player_pos'], data['player_rotation'])
			print(f"Player {data['player_id']} connected")

		elif data['request'] == 'players_list':
			for player in data['players']:
				if player['player_id'] == self.player.player_id:
					continue
				self.add_player(player['player_id'], player['player_pos'], player['player_rotation'])

		elif data['request'] == 'update_player_location':
			if data['player_id'] == self.player.player_id:
				return
			elif data['player_id'] not in self.player.connected_players:
				self.add_player(data['player_id'], data['player_pos'], data['player_rotation'])

			player_id = data['player_id']
			self.player.connected_players[player_id].position = data['player_pos']
			self.player.connected_players[player_id].rotation = data['player_rotation']
		
		elif data['request'] == 'player_disconnect':
			player_id = data['player_id']
			if player_id in self.player.connected_players:
				self.player.connected_players[player_id].enabled = False
				del self.player.connected_players[player_id]
				print(f"Player {player_id} disconnected")
		
		elif data['request'] == 'switch_weapon':
			player_id = data['player_id']
			weapon_type = data['weapon'] 
			if player_id in self.player.connected_players:
				if self.player.connected_players[player_id].current_weapon is not None:
					self.player.connected_players[player_id].current_weapon.enabled = False
				if weapon_type in self.player.connected_players[player_id].weapons_inventory:
					self.player.connected_players[player_id].current_weapon = self.player.connected_players[player_id].weapons_inventory[weapon_type]
					self.player.connected_players[player_id].current_weapon.enabled = True

			print(f"Player {player_id} switched to weapon {weapon_type}")
	


def main():
	client = Client()
	app.run()

if __name__ == '__main__':
	main()
