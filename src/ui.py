import time
import pygame
from OpenGL.GL import *


class IconButton:
    def __init__(self, x, y, size, action, image_path=None):
        self.rect = pygame.Rect(x, y, size, size)
        self.action = action
        self.texture = None

        if image_path:
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.smoothscale(image, (size, size))
            self.texture = self.load_texture(image)

    def load_texture(self, surface):
        texture = glGenTextures(1)
        texture_data = pygame.image.tostring(surface, "RGBA", True)

        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGBA,
            surface.get_width(),
            surface.get_height(),
            0, GL_RGBA, GL_UNSIGNED_BYTE,
            texture_data
        )

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        return texture

    def draw_image(self):
        if not self.texture:
            return

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)

        x, y, w, h = self.rect

        glColor4f(1, 1, 1, 1)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1); glVertex2f(x, y)
        glTexCoord2f(1, 1); glVertex2f(x + w, y)
        glTexCoord2f(1, 0); glVertex2f(x + w, y + h)
        glTexCoord2f(0, 0); glVertex2f(x, y + h)
        glEnd()

        glDisable(GL_TEXTURE_2D)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class UI:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.notification_font = pygame.font.SysFont("Arial", 15, bold=True)
        self.info_font = pygame.font.SysFont("Arial", 15, bold=True)

        self.notification = None
        self.notification_start_time = 0
        self.notification_duration = 3

        self.dropdown_open = False
        self.shape_dropdown_rect = pygame.Rect(20, self.height - 42, 190, 28)

        self.play_btn = IconButton(25, 20, 46, "toggle", "assets/ui/play.png")
        self.pause_btn = IconButton(25, 20, 46, "toggle", "assets/ui/pause.png")
        self.screenshot_btn = IconButton(82, 20, 42, "screenshot", "assets/ui/camera.png")
        self.reset_btn = IconButton(135, 20, 42, "reset", "assets/ui/reset.png")

    def show_notification(self, text):
        self.notification = text
        self.notification_start_time = time.time()

    def handle_click(self, pos, auto_rotate, shape_names):
        if auto_rotate:
            if self.pause_btn.is_clicked(pos):
                return "toggle"
        else:
            if self.play_btn.is_clicked(pos):
                return "toggle"

        if self.screenshot_btn.is_clicked(pos):
            return "screenshot"

        if self.reset_btn.is_clicked(pos):
            return "reset"

        if self.shape_dropdown_rect.collidepoint(pos):
            self.dropdown_open = not self.dropdown_open
            return None

        if self.dropdown_open:
            for index, _ in enumerate(shape_names):
                item_rect = pygame.Rect(
                    self.shape_dropdown_rect.x,
                    self.shape_dropdown_rect.y - ((index + 1) * 30),
                    self.shape_dropdown_rect.width,
                    30
                )

                if item_rect.collidepoint(pos):
                    self.dropdown_open = False
                    return ("shape", index)

            self.dropdown_open = False

        return None

    def draw_text_centered(self, text, center_x, center_y, font, color=(250, 250, 255)):
        surface = font.render(text, True, color).convert_alpha()
        text_data = pygame.image.tostring(surface, "RGBA", True)

        w = surface.get_width()
        h = surface.get_height()

        x = center_x - w / 2
        y = center_y - h / 2

        texture = glGenTextures(1)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glColor4f(1, 1, 1, 1)

        glBegin(GL_QUADS)
        glTexCoord2f(0, 1); glVertex2f(x, y)
        glTexCoord2f(1, 1); glVertex2f(x + w, y)
        glTexCoord2f(1, 0); glVertex2f(x + w, y + h)
        glTexCoord2f(0, 0); glVertex2f(x, y + h)
        glEnd()

        glDeleteTextures([texture])
        glDisable(GL_TEXTURE_2D)

    def draw_text_left(self, text, x, y, font, color=(230, 230, 240)):
        surface = font.render(text, True, color).convert_alpha()
        text_data = pygame.image.tostring(surface, "RGBA", True)

        w = surface.get_width()
        h = surface.get_height()

        texture = glGenTextures(1)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glColor4f(1, 1, 1, 1)

        glBegin(GL_QUADS)
        glTexCoord2f(0, 1); glVertex2f(x, y)
        glTexCoord2f(1, 1); glVertex2f(x + w, y)
        glTexCoord2f(1, 0); glVertex2f(x + w, y + h)
        glTexCoord2f(0, 0); glVertex2f(x, y + h)
        glEnd()

        glDeleteTextures([texture])
        glDisable(GL_TEXTURE_2D)

    def draw_rect(self, x, y, w, h, color):
        glColor4f(*color)
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + w, y)
        glVertex2f(x + w, y + h)
        glVertex2f(x, y + h)
        glEnd()

    def draw_buttons(self, auto_rotate):
        if auto_rotate:
            self.pause_btn.draw_image()
        else:
            self.play_btn.draw_image()

        self.screenshot_btn.draw_image()
        self.reset_btn.draw_image()

    def draw_shape_dropdown(self, shape_name, shape_names):
        x, y, w, h = self.shape_dropdown_rect

        self.draw_rect(x, y, w, h, (0.14, 0.17, 0.22, 0.90))
        self.draw_text_left(f"Shape: {shape_name}  ▲", x + 10, y + 7, self.info_font)

        if self.dropdown_open:
            for index, name in enumerate(shape_names):
                item_y = y - ((index + 1) * 30)

                self.draw_rect(x, item_y, w, 30, (0.18, 0.21, 0.28, 0.96))
                self.draw_text_left(name, x + 10, item_y + 8, self.info_font)

    def draw_info_panel(self, shape_name, wireframe, shape_names):
        mode = "Wireframe" if wireframe else "Solid"

        self.draw_shape_dropdown(shape_name, shape_names)

        info_text = f"Mode: {mode}  |  N: Change Shape  |  M: Toggle Mode"
        self.draw_text_left(info_text, 230, self.height - 35, self.info_font)

    def draw_notification(self):
        if not self.notification:
            return

        elapsed = time.time() - self.notification_start_time

        if elapsed > self.notification_duration:
            self.notification = None
            return

        box_w = 300
        box_h = 52
        target_x = self.width - box_w - 25
        y = 35

        if elapsed < 0.35:
            start_x = self.width + 20
            progress = elapsed / 0.35
            x = start_x + (target_x - start_x) * progress
        elif elapsed > 2.65:
            progress = (elapsed - 2.65) / 0.35
            x = target_x + (self.width + 20 - target_x) * progress
        else:
            x = target_x

        self.draw_rect(x, y, box_w, box_h, (0.14, 0.17, 0.22, 0.95))

        elapsed_ratio = min(1, elapsed / self.notification_duration)
        progress_w = box_w * elapsed_ratio

        self.draw_rect(x, y + box_h - 4, progress_w, 4, (0.70, 0.87, 0.76, 1.0))

        self.draw_text_centered(
            self.notification,
            x + box_w / 2,
            y + box_h / 2,
            self.notification_font
        )

    def draw(self, auto_rotate, shape_name, wireframe, shape_names):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, self.width, self.height, 0, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.draw_buttons(auto_rotate)
        self.draw_notification()
        self.draw_info_panel(shape_name, wireframe, shape_names)

        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)