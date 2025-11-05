from ursina import *
from player import Player
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.ursfx import ursfx
from obstacles import spawn_obstacles_recursive_task
import game_state
from contextlib import suppress

asset_folder = '.\\assets' # Path to assets
app = Ursina(title='Driver Dillema', development_mode=False, vsync=False) # Turning off vsync allows for greater framerate
level = 1 # Start at level 1, level 0 is when all other levels have been beaten

# Sun and Shader
Entity.default_shader = lit_with_shadows_shader
sun = DirectionalLight()
sun.look_at(Vec3(1,-1,-1))
sun.type = 'sun'

# Pause menu entity definitions
pause_menu = Entity(parent=camera.ui, 
                    enabled=False, 
                    ignore_paused=True, 
                    model='quad', 
                    scale=(camera.aspect_ratio, 1),
                    color=color.black,
                    alpha=128
                ) # Make pause menu Entity with camera.ui as parent for UI space
Text(parent=pause_menu, text="GAME PAUSED", origin=(0,0)).world_scale = 100
Button(parent=pause_menu, text="Resume", y=0.1, scale=(0.3, 0.05), on_click=application.resume)
Button(parent=pause_menu, text="Quit", y=-0.1, scale=(0.3, 0.05), on_click=application.quit)

# Initialize and stop level functions
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

# Global update loop function
def update():
    global level

    # Move onto next level if the player has reached the finish live
    try: 
        if player.check_if_in_finish_line():
            ursfx([(0.0, 1.0), (0.09, 0.5), (0.25, 0.5), (0.35, 0.5), (1.0, 0.0)], volume=0.75, wave='square', pitch=10, speed=2.0)
            stop_level()
            level += 1
            if not (level in (Player.SPAWN_LOCATIONS.keys())): level = 0
            invoke(init_level, level, delay=1)
    except Exception: pass

    # Pause Menu
    pause_menu.enabled = False # If the application isn't paused, hide the pause menu. (Works because update runs only when app isn't paused)
    if held_keys['escape']: # Enable pause menu when escape is pressed
        application.pause()
        pause_menu.enabled = True

# Initializate level
init_level(level)

# Bind keys
input_handler.bind('up arrow', 'w')
input_handler.bind('left arrow', 'a')
input_handler.bind('down arrow', 's')
input_handler.bind('right arrow', 'd')

# Create Sky and Run App
Sky().type = 'sky'
app.run()