from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar
import socket
import threading
import json
from ursina import Entity
from direct.actor.Actor import Actor
import random

import constants

app = Ursina(borderless=False, fullscreen=False, window_title='Client')

SERVER_IP = '127.0.0.1'
SERVER_UDP_PORT = 7878

WEAPONS= constants.WEAPONS
PLAYER_SCALE = (1,1,1)
PLAYER_COLLIDER_SCALE = (1,2.2,1)

lock = threading.Lock()
MUZZLE_FLASH_BASE_LOCATION = constants.MUZZLE_FLASH_LOCATION_PISTOL

def cam2gun_rot(camera_rot):
    gun_rot = [camera_rot[1], camera_rot[2], -camera_rot[0]]
    return gun_rot
# Class for the player's weapon
class Weapon(Entity):
	def __init__(self, camera_pivot, damage, fire_rate, ammo, magazine_size, recoil ,weapon_type ,position , rotation ,muzzle_position, fire_mode, scale = (0.4, 0.4, 0.4)):
		super().__init__()
		# Initialize the weapon's model, texture, and position in the player's hand
		self.parent = camera_pivot
		self.weapon_type = weapon_type
		self.position = Vec3(0.4, -0.3, 0.6) + position
		self.scale = scale
  
		self.muzzle = Entity(parent=self, model='cube', scale=.2,rotation = (0,-90,45), color=color.yellow)

		# self.muzzle = Entity(parent=self, model='quad', scale=(2,2,2), position = (-0.05,0.6,-1.45), color=color.yellow)

		self.rotation = rotation + constants.WEAPON_ROTATION_OFFSET
		self.damage = damage
		self.fire_rate = fire_rate
		self.ammo = ammo
		self.magazine_size = magazine_size
		self.current_ammo = self.magazine_size
		self.on_cooldown = False
		self.recoil = recoil
		self.enabled = False

		self.fire_mode = fire_mode

		self.ammo_text = Text(text=f'{self.current_ammo}/{self.ammo}', position=(-0.6,-0.3), scale=1)
		self.ammo_text.enabled = False
		
		self.muzzle.position = (muzzle_position*self.scale)
		self.muzzle.enabled = False
		
	# Function to shoot the weapon
	def shoot(self):
		if not self.on_cooldown:
			if self.current_ammo == 0:
				# self.reload()
				return False
			self.current_ammo -= 1
			self.ammo_text.text = f'{self.current_ammo}/{self.ammo}'
			hit_info = self.check_hit()
			self.display_muzzle_flash()
			self.on_cooldown = True

			invoke(setattr, self, 'on_cooldown', False, delay=0.2/self.fire_rate)
			return hit_info
		else:
			return False
		
	def display_muzzle_flash(self):
		self.muzzle.enabled = True
		invoke(setattr, self.muzzle, 'enabled', False, delay=0.1)
	
	def check_hit(self):
		# Functions checks returns player entity if hit, otherwise None
		hit_info = raycast(camera.world_position, camera.forward, distance=100 )
		if hit_info.hit:
			if hit_info.entity is not None:
				if type(hit_info.entity).__name__ == 'OtherPlayer':
					return hit_info.entity.player_id

		return None
			
	def reload(self):
		self.on_cooldown = True

		invoke(setattr, self, 'on_cooldown', False, delay=1)

		ammo_needed = self.magazine_size - self.current_ammo
		if self.ammo == 0:
			return
		if self.ammo >= ammo_needed:
			self.ammo -= ammo_needed
			self.current_ammo = self.magazine_size
		else:
			self.current_ammo += self.ammo
			self.ammo = 0

		self.current_ammo = self.magazine_size
		self.ammo_text.text = f'{self.current_ammo}/{self.ammo}'
	
	def calc_recoil(self):
		value = random.randrange(-self.recoil * 10, self.recoil * 10)
		return value / 10


class UI_Handler(Entity):
	
	def __init__(self, player):
		super().__init__(
			parent = camera.ui,                                                                                   
			)
		self.player = player
		
		
		self.health_bar = HealthBar(max_value = player.health)
		self.ammo_text = Text(text=f'', position=(-0.6,-0.3), scale=1)

	def update(self):
		if self.health_bar.value != self.player.health:
			self.health_bar.value = self.player.health
	
	def show_ammo(self):
		self.ammo_text.enabled = True
	
	def hide_ammo(self):
		self.ammo_text.enabled = False
	
	def update_ammo(self):
		self.ammo_text.text = f'{self.player.current_weapon.current_ammo}/{self.player.current_weapon.ammo}'


class Pistol(Weapon):
	def __init__(self, camera_pivot,muzzle_position, position = (0,0,0), rotation = (0,0,0), scale = (0.3, 0.3, 0.3)):
		super().__init__(camera_pivot,
					damage = WEAPONS["Pistol"]["damage"],
					fire_rate = WEAPONS["Pistol"]["fire_rate"],
					ammo = WEAPONS["Pistol"]["ammo"],
					magazine_size = WEAPONS["Pistol"]["magazine_size"],
					weapon_type = "Pistol",
					recoil = WEAPONS["Pistol"]["recoil"],
					position=position, rotation=rotation, scale=scale, muzzle_position=muzzle_position,
					fire_mode="semi")
					
		self.model = 'Assets/Models/Pistol.obj'
		
class AssaultRifle(Weapon):
	def __init__(self, camera_pivot,muzzle_position, position = (0,0,0), rotation = (0,0,0), scale = (0.3, 0.3, 0.3)):
		super().__init__(camera_pivot,
					damage = WEAPONS["Assault Rifle"]["damage"],
					fire_rate = WEAPONS["Assault Rifle"]["fire_rate"],
					ammo = WEAPONS["Assault Rifle"]["ammo"],
					magazine_size = WEAPONS["Assault Rifle"]["magazine_size"],
					weapon_type = "Assault Rifle",
					recoil = WEAPONS["Assault Rifle"]["recoil"],
					position=position, rotation=rotation, scale=scale, muzzle_position=muzzle_position,
					fire_mode="full")
					
		self.model = 'Assets/Models/Assault.obj'


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

		self.weapon_inventory = [Pistol(self.controller.camera_pivot, muzzle_position=constants.MUZZLE_FLASH_LOCATION_RIFLE),
						    AssaultRifle(self.controller.camera_pivot, muzzle_position=constants.MUZZLE_FLASH_LOCATION_RIFLE)]
		self.current_weapon = None
	
		self.create_ground()
		self.create_connection()

		
		self.game_running = True
		
		self.connected_players = {}

		self.ui_handler = UI_Handler(self)
		

	def create_connection(self):

		# Create a UDP socket and connect to the server
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.settimeout(5)
		self.sock.connect((SERVER_IP, SERVER_UDP_PORT))
		self.send_hello()
		# Save the player's ID
		while self.player_id is None:
			data = self.sock.recv(65535)
			if data:
				data = json.loads(data.decode())
				self.player_id = data['player_id']

	def create_ground(self):
		model = load_model("Assets/untitled")
		# ground = Entity(model='plane', texture='grass', scale=(100, 100, 100), position=(0, -5, 0), collider='box')
		ground = Entity(model=model, scale=(10,10,10), position=(0, -5, 0), collider='mesh')

	def change_fov(self, fov):
		camera.fov = lerp(camera.fov, fov, 8 * time.dt)

	def check_state(self):
		self.prev_state = self.state
		distance = self.controller.position - self.prev_location
		if abs(distance.x) > 0.01 or abs(distance.z) > 0.01 and self.controller.grounded:
			self.state = "moving"
		elif self.controller.position != self.prev_location and not self.controller.grounded:
			self.state = "airborne"
		else:
			self.state = "idle"

	
	def equip_weapon(self, index=0):
		if index >= len(self.weapon_inventory):
			return None
		
		# If the player has the weapon equipped, unequip it
		if self.current_weapon == self.weapon_inventory[index]:
			self.current_weapon.enabled = False
			self.ui_handler.hide_ammo()
			self.current_weapon = None
			

		# If the player has another weapon equipped, unequip it and equip the new weapon
		elif self.current_weapon is not None:
			self.current_weapon.enabled = False
			self.current_weapon = self.weapon_inventory[index]
			self.current_weapon.enabled = True
			self.ui_handler.update_ammo()

		# Equip the weapon
		elif self.weapon_inventory[index] is not None:
			self.current_weapon = self.weapon_inventory[index]
			self.current_weapon.enabled = True
			self.ui_handler.show_ammo()
			self.ui_handler.update_ammo()

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
		camera_rot = self.controller.camera_pivot.rotation
		
		request = json.dumps(
			{
				"request": "update_location",
				"player_id": self.player_id,
				"player_pos": [player_pos.x, player_pos.y, player_pos.z],
				"player_rotation": [player_rot.x, player_rot.y, player_rot.z],
				"camera_rotation": [camera_rot.x, camera_rot.y, camera_rot.z],
				"player_state": self.state
			}
		)

		self.sock.sendall(request.encode())

	def send_hello(self):
		hello_request = self.build_request("hello")
		self.sock.sendall(hello_request.encode())

	def build_request(self, request_type, **kwargs):
		if request_type == "hello":
			player_pos = self.controller.position
			player_rot = self.controller.rotation
			camera_rot = self.controller.camera_pivot.rotation

			request = json.dumps(
				{
					"request": "hello",
					"player_pos": [player_pos.x, player_pos.y, player_pos.z],
					"player_rotation": [player_rot.x, player_rot.y, player_rot.z],
					"camera_rotation": [camera_rot.x, camera_rot.y, camera_rot.z]
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

		elif request_type == "shoot":
			request = json.dumps(
				{
					"request": "shoot",
					"player_id": self.player_id,
					"hit_player": kwargs['hit_player'] if 'hit_player' in kwargs else None,
					"weapon_type": self.current_weapon.weapon_type
				}
			)
		return request
	
	def input(self, key):
		if key == 'escape':
			self.send_disconnect()
		if key == '1':
			self.equip_weapon(0)
		if key == '2':
			self.equip_weapon(1)
		if key == '3':
			self.equip_weapon(2)
		
		if key == 'r':
			self.current_weapon.reload()
			invoke(self.ui_handler.update_ammo, delay=1)
			
		
		if key == 'left mouse down':
			if self.current_weapon is not None:
				self.shoot_weapon()
		
	def update(self):
		
		self.check_state()

		if self.state != self.prev_state or self.controller.position != self.prev_location or self.controller.rotation != self.prev_rotation:
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
		
		# Handle full auto weapons
		if held_keys['left mouse']:
			if self.current_weapon is not None:
				if self.current_weapon.fire_mode == "full":
					
					if self.current_weapon is not None:
						self.shoot_weapon()

		self.prev_location = self.controller.position
		self.prev_rotation = self.controller.rotation
	
	def shoot_weapon(self):
		if self.current_weapon is not None:
				shoot_data = self.current_weapon.shoot()
				# shoot_data meaning:
				# False - Didn't shoot
				# None - Hit nothing
				# dictionary - Hit
				self.ui_handler.update_ammo()
				
				if shoot_data is not False:
					request = self.build_request("shoot", hit_player=shoot_data)
					self.sock.sendall(request.encode())
				

	def death_screen(self):
		# Create a death screen
		death_screen = Entity(model='quad', scale=(2, 1), color=color.black, z=-1)
		death_text = Text(text='You have died', scale=2, y=0.1, color=color.red)
		death_text.create_background(padding=(.5,.25), radius=Text.size/2)
		invoke(self.send_disconnect, delay=6)


	def send_disconnect(self):
		# Function to start the process of disconnecting
		request = self.build_request("disconnect")
		self.sock.sendall(request.encode())
		# Closes the application on client side, lets server side know of disconnect
		application.quit()


class Client():
	def __init__(self):
		self.player = Player()

		sky = Sky()

		listen_thread = threading.Thread(target=self.listen)
		listen_thread.start()
	
	def listen(self):
		while True:
			if not self.player.game_running:
				self.player.sock.close()
				break
			else:
				try:
					data, addr = self.player.sock.recvfrom(65535)
					if addr == (SERVER_IP, SERVER_UDP_PORT) and data:
						self.handle_request(data)
				except socket.timeout:
					# Close game, no connection to server
					pass
	
	def add_player(self, player_id, player_pos, player_rotation):
		self.player.connected_players[player_id] = OtherPlayer(player_id, player_pos, player_rotation)
	

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
			player_pos = Vec3(data['player_pos'][0], data['player_pos'][1], data['player_pos'][2])
			player_rot = Vec3(data['player_rotation'][0], data['player_rotation'][1], data['player_rotation'][2])

			self.add_player(player_id,player_pos, player_rot)
			print(f"Player {player_id} connected")

		elif data['request'] == 'players_list':
			for player in data['players']:

				if player['player_id'] == self.player.player_id:
					continue

				player_id = player['player_id']
				player_pos = Vec3(player['player_pos'][0], player['player_pos'][1], player['player_pos'][2])
				player_rot = Vec3(player['player_rotation'][0], player['player_rotation'][1], player['player_rotation'][2])

				weapon_type = player['weapon']

				self.add_player(player_id,player_pos, player_rot)
				self.player.connected_players[player_id].equip(weapon_type)
    

    
				if self.player.connected_players[player_id].current_weapon is not None:
					weapon_rotation = cam2gun_rot(player['camera_rotation'])
					self.player.connected_players[player_id].current_weapon.rotation = weapon_rotation + list(constants.WEAPON_ROTATION_OFFSET)

		elif data['request'] == 'update_player_location':
			if data['player_id'] == self.player.player_id:
				return
			elif data['player_id'] not in self.player.connected_players:
				self.add_player(data['player_id'], data['player_pos'], data['player_rotation'])

			player_id = data['player_id']
			player_state = data['player_state']

			self.player.connected_players[player_id].position = data['player_pos']
			self.player.connected_players[player_id].rotation = data['player_rotation']
			if self.player.connected_players[player_id].current_weapon is not None:
				weapon_rotation = cam2gun_rot(data['camera_rotation'])
				self.player.connected_players[player_id].current_weapon.rotation = weapon_rotation + list(constants.WEAPON_ROTATION_OFFSET)

				# self.player.connected_players[player_id].current_weapon.rotation = [data['camera_rotation'][1], data['camera_rotation'][2], -data['camera_rotation'][0]] + list(constants.WEAPON_ROTATION_OFFSET)

   
			if player_state == "moving" and self.player.connected_players[player_id].state != "moving":
				self.player.connected_players[player_id].actor.loop('Run')
				self.player.connected_players[player_id].state = "moving"

			elif player_state == "idle" and self.player.connected_players[player_id].state != "idle":
				self.player.connected_players[player_id].actor.loop('Idle')
				self.player.connected_players[player_id].state = "idle"

			elif player_state == "airborne" and self.player.connected_players[player_id].state != "airborne":
				self.player.connected_players[player_id].actor.loop('Idle')
				self.player.connected_players[player_id].state = "airborne"
		
		elif data['request'] == 'player_disconnect':
			player_id = data['player_id']
			# If the disconnecting player exists in our game
			if player_id in self.player.connected_players:
				self.player.connected_players[player_id].enabled = False
				del self.player.connected_players[player_id]
				print(f"Player {player_id} disconnected")
			# If the disconnecting player is us, close the connection socket
			elif player_id == self.player.player_id:
				self.player.game_running = False


		
		elif data['request'] == 'switch_weapon':
			player_id = data['player_id']
			weapon_type = data['weapon'] 
			if player_id in self.player.connected_players:
				self.player.connected_players[player_id].equip(weapon_type)

			print(f"Player {player_id} switched to weapon {weapon_type}")

		elif data['request'] == 'player_shoot':
			player_id = data['player_id']
			weapon_type = data['weapon_type']
			hit_player = data['hit_player']

			self.player.connected_players[player_id].current_weapon.display_muzzle_flash()
			if isinstance(hit_player, int):
				if hit_player != self.player.player_id:
					if hit_player in self.player.connected_players:
						hit_player_obj = self.player.connected_players[hit_player]
						print(f"Player {player_id} shot player {hit_player} with weapon {weapon_type}")
						
						if hit_player_obj.health > 0:
							hit_player_obj.health -= WEAPONS[weapon_type]['damage']
							if hit_player_obj.health <= 0:
								hit_player_obj.enabled = False
								del self.player.connected_players[hit_player]
								print(f"Player {hit_player} has been killed")
						else:
							print(f"Player {hit_player} is already dead")
					else:
						print(f"Player {hit_player} is not connected")
						
				elif hit_player == self.player.player_id:
					print(f"Player {player_id} shot you with weapon {weapon_type}")
					if self.player.health > 0:
						self.player.health -= WEAPONS[weapon_type]['damage']
						if self.player.health <= 0:
							print(f"You have been killed")
							self.player.death_screen()

					else:
						print(f"You are already dead")

class OtherPlayer(Entity):
	def __init__(self, player_id, player_pos, player_rotation):
		super().__init__()
		self.actor = Actor('Assets/Models/Chicken.gltf')
		self.actor.reparent_to(self)
		self.player_id = player_id
		self.position = player_pos
		self.rotation = Vec3(player_rotation[0], player_rotation[1], player_rotation[2])
	

		self.state = "idle"
		self.collider = BoxCollider(self, center=(0,1,0), size=(1,2,1))
		
		self.scale = PLAYER_SCALE
		self.name = str(player_id)

		self.health = 100
		self.weapons_inventory = {"Pistol": Pistol(self,muzzle_position=constants.MUZZLE_FLASH_LOCATION_PISTOL_OTHER, scale=0.7, position=(0.25,1.2,-0.3), rotation=(0,0,0)),
							 "Assault Rifle": AssaultRifle(self,muzzle_position=constants.MUZZLE_FLASH_LOCATION_RIFLE_OTHER, scale=0.7, position=(0.25,1.2,-0.3), rotation=(0,0,0))}
		self.current_weapon = None
		self.enabled = True
	

		self.actor.loop('Idle')

	def equip(self, weapon_type):
		if self.current_weapon is not None:
			self.current_weapon.enabled = False
		if weapon_type in self.weapons_inventory:
			self.current_weapon = self.weapons_inventory[weapon_type]
			self.current_weapon.enabled = True

def main():
	client = Client()
	app.run()

if __name__ == '__main__':
	main()
