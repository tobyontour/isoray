import numpy as np
import math
from .utils import normalize

class Solid:
    material = None

    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
        self.material = Material()

    def normal_to_surface(self, intersection):
        return normalize(intersection - self.center)

    def intersect(self, ray_origin, ray_direction):
        b = 2 * np.dot(ray_direction, ray_origin - self.center)
        c = np.linalg.norm(ray_origin - self.center) ** 2 - self.radius ** 2
        delta = b ** 2 - 4 * c
        if delta > 0:
            t1 = (-b + np.sqrt(delta)) / 2
            t2 = (-b - np.sqrt(delta)) / 2
            if t1 > 0 and t2 > 0:
                return min(t1, t2)
        return None

class Material():
    shininess = 100
    reflection = 0.5

    def __init__(self, red: float = 0.0, green: float = 0.0, blue: float = 0.0):
        self.ambient = np.array([red, green, blue])
        self.diffuse = np.array([red, green, blue])
        self.specular = np.array([1, 1, 1])

class Sphere(Solid):
    pass

class Plane(Solid):
    def __init__(self, point, normal):
        self.point = point
        self.normal = normalize(normal)
        self.material = Material()

    def normal_to_surface(self, intersection):
        return self.normal

    def intersect(self, ray_origin, ray_direction):
        # assuming vectors are all normalized
        denom = np.dot(self.normal, ray_direction)
        if denom < -1e-5:
            w = ray_origin - self.point
            si = np.dot(-self.normal, w) / denom
            Psi = w + si * ray_direction + self.point
            return math.sqrt(Psi[0] ** 2 + Psi[1] ** 2 + Psi[2] ** 2)

        return None

