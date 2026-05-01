from OpenGL.GL import *
from objects.base_shape import BaseShape


class Pyramid(BaseShape):
    def __init__(self):
        super().__init__()

        self.name = "Pyramid"

        self.vertices = [
            (-1, -1, -1),
            (1, -1, -1),
            (1, -1, 1),
            (-1, -1, 1),
            (0, 1.2, 0)
        ]

        self.faces = [
            (0, 1, 2, 3),
        ]

        self.triangles = [
            (0, 1, 4),
            (1, 2, 4),
            (2, 3, 4),
            (3, 0, 4),
        ]

        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (0, 4), (1, 4), (2, 4), (3, 4)
        ]

        self.colors = [
            (0.95, 0.67, 0.67),
            (0.70, 0.87, 0.76),
            (0.67, 0.78, 0.95),
            (0.96, 0.86, 0.62),
            (0.78, 0.68, 0.90),
        ]

    def draw_solid(self):
        glBegin(GL_QUADS)
        glColor3fv(self.colors[0])
        for vertex in self.faces[0]:
            glVertex3fv(self.vertices[vertex])
        glEnd()

        glBegin(GL_TRIANGLES)
        for i, triangle in enumerate(self.triangles):
            glColor3fv(self.colors[(i + 1) % len(self.colors)])
            for vertex in triangle:
                glVertex3fv(self.vertices[vertex])
        glEnd()