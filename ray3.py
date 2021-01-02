import numpy as np
import pygame
from lib.solid import Sphere, Plane
import lib.utils as utils
from lib.renderer import Renderer

pygame.init()

width = 320
height = 200

screen = pygame.display.set_mode((width, height))
screen.fill((50, 50, 50))
pygame.display.flip()

objects = []

data = [
    { 'center': np.array([-0.2, 0, -1]), 'radius': 0.7, 'ambient': np.array([0.1, 0, 0]), 'diffuse': np.array([0.7, 0, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 50, 'reflection': 0.5 },
    { 'center': np.array([0.1, -0.3, 0]), 'radius': 0.1, 'ambient': np.array([0.1, 0, 0.1]), 'diffuse': np.array([0.7, 0, 0.7]), 'specular': np.array([1, 1, 1]), 'shininess': 80, 'reflection': 0.5 },
    { 'center': np.array([-0.3, 0, 0]), 'radius': 0.15, 'ambient': np.array([0, 0.1, 0]), 'diffuse': np.array([0, 0.6, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5 },
    # { 'center': np.array([0, -9000, 0]), 'radius': 9000 - 0.7, 'ambient': np.array([0.1, 0.1, 0.8]), 'diffuse': np.array([0.6, 0.6, 0.6]), 'specular': np.array([1, 1, 1]), 'shininess': 40, 'reflection': 0.1 }
]

for s in data:
    sphere = Sphere(s['center'], s['radius'])
    sphere.material.ambient = s['ambient']
    sphere.material.diffuse = s['diffuse']
    sphere.material.specular = s['specular']
    objects.append(sphere)

p = Plane(np.array([0, -1.1, 0]), np.array([0, 1.0, 0]))
p.material.ambient = np.array([0, 0.1, 0.1])
p.material.diffuse = np.array([0, 0.7, 0.7])
p.material.specular = np.array([1, 1, 1])
objects.append(p)

renderer = Renderer(screen, width, height, 5)
renderer.render(objects)

quit = False
while not quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True

pygame.quit();
