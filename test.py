from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from direct.filter.CommonFilters import CommonFilters



app = Ursina()

outline_shader = Shader(
    fragment = open('Assets/Shaders/outline/outline.frag').read(),
    default_input = {
        'outline_size': 0.001,
        'aspect_ratio': window.aspect_ratio
    }
)

cellshading_shader = Shader(
    vertex= open('Assets/Shaders/outline/cellshading.vert').read(),
    fragment = open('Assets/Shaders/outline/cellshading.frag').read(),
    default_input = {
        'avg_precision' : 5,
        "brightness" : 1,
        "atmosphere_light" : 0.5,
        "palette_size" :2,
        "light_direction" : Vec3(0,-1,0),
    }
)

random.seed(0)
Entity.default_shader = cellshading_shader

ground = Entity(model='plane', collider='box', scale=64, texture='grass', texture_scale=(4,4))

editor_camera = EditorCamera(enabled=False, ignore_paused=True)
player = FirstPersonController(model='cube', z=-10, color=color.orange, origin_y=-.5, speed=8, collider='box')
player.collider = BoxCollider(player, Vec3(0,1,0), Vec3(1,2,1))

shootables_parent = Entity()
mouse.traverse_target = shootables_parent


for i in range(16):
    a = Entity(model='cube', origin_y=-.5, scale=2, texture='brick', texture_scale=(1,2),
        x=random.uniform(-8,8),
        z=random.uniform(-8,8) + 8,
        collider='box',
        scale_y = random.uniform(2,3),
        color=color.hsv(0, 0, random.uniform(.9, 1))
        )

sun = DirectionalLight()
sun.look_at(Vec3(1,-1,-1))
Sky()


camera.shader = outline_shader

app.run()