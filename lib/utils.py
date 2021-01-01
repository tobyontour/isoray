import numpy as np

def normalize(vector):
    return vector / np.linalg.norm(vector)

def reflected(vector, axis):
    return vector - 2 * np.dot(vector, axis) * axis

def toRgb(color):
    red = np.clip(int(color[0] * 255), 0, 255)
    green = np.clip(int(color[1] * 255), 0, 255)
    blue = np.clip(int(color[2] * 255), 0, 255)
    return (red, green, blue)

def nearest_intersected_object(objects, ray_origin, ray_direction):
    distances = [obj.intersect(ray_origin, ray_direction) for obj in objects]
    nearest_object = None
    min_distance = np.inf
    for index, distance in enumerate(distances):
        if distance and distance < min_distance:
            min_distance = distance
            nearest_object = objects[index]
    return nearest_object, min_distance