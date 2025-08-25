from ursina import *
from player import Player
from ursina.shaders import lit_with_shadows_shader
from obstacles import spawn_cars_task, spawn_spheres_task

asset_folder = '.\\assets'
app = Ursina(title='Driver Dillema')
Entity.default_shader = lit_with_shadows_shader

level = 1
player = Player(level)
player.spawn()

level_base = Entity(model='level-base', texture=f'level{level}', collider='box')
level_base.scale_setter(5)
level_base.rotate((0, 180, 0))
level_base.type = 'lb'

try:
    level_extras = Entity(model=load_model(f'level{level}'), texture='grass')
    level_extras.scale_setter(5)
    level_extras.rotate((0, 180, 0))
    level_extras.collision = True
    level_extras.collider_setter('mesh')
    level_extras.type = 'le'
except FileNotFoundError:
    pass

sun = DirectionalLight()
sun.look_at(Vec3(1,-1,-1))
sun.type = 'sun'

spawn_spheres_task(level)
spawn_cars_task(level)

input_handler.bind('up arrow', 'w')
input_handler.bind('left arrow', 'a')
input_handler.bind('down arrow', 's')
input_handler.bind('right arrow', 'd')

Sky().type = 'sky'
app.run()