from ursina import *
from player import Player
from ursina.shaders import lit_with_shadows_shader

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

# Sphere task
def spawn_sphere(vel, pos):
    sphere = Entity(model='sphere', color=color.red, scale=0.5, position=pos)
    sphere.velocity = Vec3(vel, 0, 0)
    sphere.type = 'obstacle'

    def update():
        sphere.position += sphere.velocity * time.dt
        sphere.collider_setter(SphereCollider(sphere, (0, 0, 0), 2))

        if abs(sphere.x) >= 8:
            sphere.disable()

    sphere.update = update

def spawn_spheres_task():
    if level == 1:
        spawn_sphere(-6, (7, 0.75, -0.25))
        spawn_sphere(6, (-7, 0.75, 0.5))
    elif level == 2:
        spawn_sphere(-6, (7, 0.75, 4.3))
        spawn_sphere(6, (-7, 0.75, 5))
    elif level == 3:
        spawn_sphere(-6, (7, 0.75, 4.2))
        spawn_sphere(6, (-7, 0.75, 4.9))
        spawn_sphere(-6, (7, 0.75, -5.3))
        spawn_sphere(6, (-7, 0.75, -4.5))
    invoke(spawn_spheres_task, delay=0.65)

# Cars task
def spawn_car(vel, pos):
    car = Entity(model='player.obj', texture='car', position=pos)
    car.velocity = Vec3(vel, 0, 0)
    car.type = 'obstacle'
    direction = -1 if vel > 0 else 1
    car.rotation_setter((0, 90 * direction, 0))

    def update():
        car.position += car.velocity * time.dt
        car.collider_setter(BoxCollider(car, (0, 0, 0), (1, 1, 1)))

        if abs(car.x) >= 8:
            car.disable()

    car.update = update

def spawn_cars_task():
    # Level 1 has no cars
    if level == 2:
        spawn_car(-5, (7, 0.25, -2))
        spawn_car(5, (-7, 0.25, -0.5))
    elif level == 3:
        spawn_car(-6, (7, 0.25, 1.3))
        spawn_car(6, (-7, 0.25, -0.1))
        spawn_car(-6, (7, 0.25, -1.7))

    invoke(spawn_cars_task, delay=0.65)

spawn_spheres_task()
spawn_cars_task()

Sky().type = 'sky'
app.run()