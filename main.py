from ursina import *
from player import Player
from ursina.shaders import lit_with_shadows_shader
from obstacles import spawn_obstacles_recursive_task
import game_state
from contextlib import suppress

asset_folder = '.\\assets'
app = Ursina(title='Driver Dillema')
Entity.default_shader = lit_with_shadows_shader

sun = DirectionalLight()
sun.look_at(Vec3(1,-1,-1))
sun.type = 'sun'

label_base = None
level_extras = None
player = None

def init_level(level):
    global player, level_base, level_extras

    game_state.level_running = True
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

    spawn_obstacles_recursive_task(level)

def stop_level():
    global player, level_base, level_extras
    for i in [player, level_base, level_extras]: 
        with suppress(Exception): destroy(i)
    player = None
    level_base = None
    level_extras = None
    game_state.level_running = False
    [destroy(i) for i in scene.children if hasattr(i, 'type') and i.type == 'obstacle']

def update():
    global level

    try: 
        if player.check_if_in_finish_line():
            stop_level()
            level += 1
            invoke(init_level, level, delay=1)
    except Exception: pass

level = 1
init_level(level) # Start with level 1

input_handler.bind('up arrow', 'w')
input_handler.bind('left arrow', 'a')
input_handler.bind('down arrow', 's')
input_handler.bind('right arrow', 'd')

Sky().type = 'sky'
app.run()