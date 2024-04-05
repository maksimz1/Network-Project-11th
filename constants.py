# File to store all the weapon constants
from ursina import *
WEAPONS = {
    "Pistol": {
        "damage": 20,
        "fire_rate": 0.5,
        "magazine_size": 15,
        "ammo": 60,

    },
    "Shotgun": {
        "damage": 30,
        "fire_rate": 0.4,
        "magazine_size": 5,
        "ammo": 20,
    },
    "Assault Rifle": {
        "damage": 15,
        "fire_rate": 1.0,
        "magazine_size": 30,
        "ammo": 90,
    },
}
MUZZLE_FLASH_TIME = 0.1
WEAPON_ROTATION_OFFSET = (0, 90, 0)
MUZZLE_FLASH_LOCATION_PISTOL= ((-1.6 / 0.3),(0.6 / 0.3),(0 / 0.3))
MUZZLE_FLASH_LOCATION_PISTOL_OTHER = ((-0.66 / 0.3),(0.22 / 0.3),(0 / 0.3))