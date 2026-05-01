from OpenGL.GL import *


class Renderer:
    def __init__(self):
        glEnable(GL_DEPTH_TEST)

    def clear(self, background_color):
        glClearColor(*background_color)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def draw_grid(self, size=10, step=1):
        glLineWidth(1)
        glColor3f(0.28, 0.28, 0.34)
        glBegin(GL_LINES)

        for i in range(-size, size + 1, step):
            glVertex3f(i, -2, -size)
            glVertex3f(i, -2, size)

            glVertex3f(-size, -2, i)
            glVertex3f(size, -2, i)

        glEnd()