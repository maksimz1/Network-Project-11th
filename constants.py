# File to store all game constants
from ursina import *

# Weapon constants
WEAPONS = {
    "Pistol": {
        "damage": 20,
        "fire_rate": 0.5,
        "magazine_size": 15,
        "ammo": 60,
        "recoil": 0.4

    },
    "Shotgun": {
        "damage": 30,
        "fire_rate": 0.4,
        "magazine_size": 5,
        "ammo": 20,
        "recoil": 1
    },
    "Assault Rifle": {
        "damage": 15,
        "fire_rate": 2.0,
        "magazine_size": 30,
        "ammo": 90,
        "recoil": 0.8
    },
}

MUZZLE_FLASH_TIME = 0.1
WEAPON_ROTATION_OFFSET = (0, 90, 0)
MUZZLE_FLASH_LOCATION_PISTOL= ((-1.6 / 0.3),(0.6 / 0.3),(0 / 0.3))
MUZZLE_FLASH_LOCATION_PISTOL_OTHER = ((-0.66 / 0.3),(0.22 / 0.3),(0 / 0.3))

MUZZLE_FLASH_LOCATION_RIFLE= ((-3 / 0.3),(0.25 / 0.3),(0 / 0.3))
MUZZLE_FLASH_LOCATION_RIFLE_OTHER = ((-1.275 / 0.3),(0.09 / 0.3),(0 / 0.3))

KEEP_ALIVE_TIME = 1
TIMEOUT_TIME = 2

# Player constants
SPAWN_POS = Vec3(0, 0, 0)
SPAWN_ROT = Vec3(0, 0, 0)

