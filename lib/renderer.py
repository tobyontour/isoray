
import numpy as np
import pygame
from lib.solid import Sphere
import lib.utils as utils

class Renderer:

    def __init__(self, display, width, height, max_depth = 3):
        self.display = display
        self.width = width
        self.height = height
        self.max_depth = 3
        self.camera = np.array([0, 0, 1])
        self.lights = [
            { 'position': np.array([5, 5, 5]), 'ambient': np.array([0.8, 0.8, 0.8]), 'diffuse': np.array([1, 1, 1]), 'specular': np.array([1, 1, 1]) },
            # { 'position': np.array([-5, 2, 5]), 'ambient': np.array([0.8, 0.8, 0.8]), 'diffuse': np.array([1, 1, 1]), 'specular': np.array([1, 1, 1]) }
        ]

    def render(self, objects):
        camera = self.camera
        ratio = float(self.width) / self.height
        screen = (-1, 1 / ratio, 1, -1 / ratio) # left, top, right, bottom

        for i, y in enumerate(np.linspace(screen[1], screen[3], self.height)):
            for j, x in enumerate(np.linspace(screen[0], screen[2], self.width)):
                # screen is on origin
                pixel = np.array([x, y, 0])
                # origin =  np.array([x, y, 1])
                origin = camera
                direction = utils.normalize(pixel - origin)

                color = np.zeros((3))
                reflection = 1

                for k in range(self.max_depth):
                    # check for intersections
                    nearest_object, min_distance = utils.nearest_intersected_object(objects, origin, direction)
                    if nearest_object is None:
                        break

                    intersection = origin + min_distance * direction
                    # normal_to_surface = utils.normalize(intersection - nearest_object.center)
                    normal_to_surface = nearest_object.normal_to_surface(intersection)
                    shifted_point = intersection + 1e-5 * normal_to_surface

                    for light in self.lights:

                        intersection_to_light = utils.normalize(light['position'] - shifted_point)

                        _, min_distance = utils.nearest_intersected_object(objects, shifted_point, intersection_to_light)
                        intersection_to_light_distance = np.linalg.norm(light['position'] - intersection)
                        is_shadowed = min_distance < intersection_to_light_distance

                        if is_shadowed:
                            break

                        illumination = np.zeros((3))

                        # ambiant
                        illumination += nearest_object.material.ambient * light['ambient']

                        # diffuse
                        illumination += nearest_object.material.diffuse * light['diffuse'] * np.dot(intersection_to_light, normal_to_surface)

                        # specular
                        intersection_to_camera = utils.normalize(camera - intersection)
                        H = utils.normalize(intersection_to_light + intersection_to_camera)
                        illumination += nearest_object.material.specular * light['specular'] * np.dot(normal_to_surface, H) ** (nearest_object.material.shininess / 4)

                        # reflection
                        color += reflection * illumination
                        reflection *= nearest_object.material.reflection

                    origin = shifted_point
                    direction = utils.reflected(direction, normal_to_surface)

                # image[i, j] = np.clip(color, 0, 1)
                self.display.set_at((j, i), utils.toRgb(color))
            print("%d/%d" % (i + 1, self.height))
            pygame.display.flip()
