from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

class Player(Entity):
    def __init__(self):
        super().__init__()
        self.speed = 2.5
        self.jump_height = 0.5
        self.gravity = 0.5
        self.jumping = False

        self.controller = FirstPersonController()

        self.create_ground()

    def create_ground(self):
        ground = Entity(model=r'Assets\ground.obj',texture = 'Assets\Grass.jpg', scale=(1, 1, 1), position=(0, -5, 0), collider='mesh')

    def change_fov(self,fov):
        camera.fov = lerp(camera.fov, fov, 8 * time.dt)

    def update(self):
        print(self.controller.grounded)
        print(camera.fov)
        if held_keys['shift'] and self.controller.grounded:
            # Increase the player speed and fov
            self.change_fov(110)
            self.controller.speed = 10
            print("running")
        else:
            # Reset the player speed and fov
            self.change_fov(80)
            self.controller.speed = 5


class Client():
    def __init__(self):
        self.player = Player()

        sky = Sky()

client = Client()
app.run()










