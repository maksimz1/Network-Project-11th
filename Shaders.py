from ursina import *
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