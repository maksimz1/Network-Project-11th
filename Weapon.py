
from ursina.shaders import *
from ursina import *
import constants

WEAPONS= constants.WEAPONS

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
		self.shader = colored_lights_shader

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