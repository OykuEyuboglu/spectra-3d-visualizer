from OpenGL.GL import glTranslatef


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = -8

        self.speed = 0.12
        self.zoom_speed = 0.4

    def apply(self):
        glTranslatef(self.x, self.y, self.z)

    def move_left(self):
        self.x += self.speed

    def move_right(self):
        self.x -= self.speed

    def move_up(self):
        self.y -= self.speed

    def move_down(self):
        self.y += self.speed

    def zoom_in(self):
        self.z += self.zoom_speed

    def zoom_out(self):
        self.z -= self.zoom_speed