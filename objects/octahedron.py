from OpenGL.GL import *
from objects.base_shape import BaseShape


class Octahedron(BaseShape):
    def __init__(self):
        super().__init__()

        self.name = "Octahedron"

        self.vertices = [
            (0, 1.3, 0),
            (1, 0, 0),
            (0, 0, 1),
            (-1, 0, 0),
            (0, 0, -1),
            (0, -1.3, 0)
        ]

        self.triangles = [
            (0, 1, 2),
            (0, 2, 3),
            (0, 3, 4),
            (0, 4, 1),
            (5, 2, 1),
            (5, 3, 2),
            (5, 4, 3),
            (5, 1, 4),
        ]

        self.edges = [
            (0, 1), (0, 2), (0, 3), (0, 4),
            (5, 1), (5, 2), (5, 3), (5, 4),
            (1, 2), (2, 3), (3, 4), (4, 1)
        ]

        self.colors = [
            (0.95, 0.67, 0.67),
            (0.70, 0.87, 0.76),
            (0.67, 0.78, 0.95),
            (0.96, 0.86, 0.62),
            (0.78, 0.68, 0.90),
            (0.64, 0.88, 0.88),
        ]

    def draw_solid(self):
        glBegin(GL_TRIANGLES)
        for i, triangle in enumerate(self.triangles):
            glColor3fv(self.colors[i % len(self.colors)])
            for vertex in triangle:
                glVertex3fv(self.vertices[vertex])
        glEnd()