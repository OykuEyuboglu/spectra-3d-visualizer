from OpenGL.GL import *


class BaseShape:
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.edges = []
        self.colors = []

    def draw_solid(self):
        glBegin(GL_QUADS)
        for i, face in enumerate(self.faces):
            glColor3fv(self.colors[i % len(self.colors)])
            for vertex in face:
                glVertex3fv(self.vertices[vertex])
        glEnd()

    def draw_wireframe(self):
        glColor3f(0.92, 0.92, 0.96)
        glLineWidth(2)

        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()

    def draw(self, wireframe=False):
        if not wireframe:
            self.draw_solid()

        self.draw_wireframe()