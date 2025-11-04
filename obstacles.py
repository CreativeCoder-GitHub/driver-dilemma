"""
`game_state` module

This module is responsible for summoning and moving obstacles. 
It also contains the `spawn_obstacles_recursive_task` function that repeatedly spawns obstacles for a certain level.
"""

from ursina import *
import game_state

# Functions to Spawn Obstacles
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

# Functions to Spawn Obstacles at Certain Locations Based on Level Selected
def spawn_spheres_task(level):
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

def spawn_cars_task(level):    
    # NOTE: Level 1 has no cars
    if level == 2:
        spawn_car(-5, (7, 0.25, -2))
        spawn_car(5, (-7, 0.25, -0.5))
    elif level == 3:
        spawn_car(-6, (7, 0.25, 1.3))
        spawn_car(6, (-7, 0.25, -0.1))
        spawn_car(-6, (7, 0.25, -1.7))

# Function to Repeatedly Spawn Obstacles Based on Level Selected
def spawn_obstacles_recursive_task(level):
    if not game_state.level_running: return # Stop when level_running is False
    
    spawn_cars_task(level)
    spawn_spheres_task(level)

    invoke(spawn_obstacles_recursive_task, level, delay=0.65)