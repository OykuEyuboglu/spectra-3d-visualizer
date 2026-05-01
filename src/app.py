import os
from datetime import datetime

import pygame
from pygame.locals import *

from PIL import Image

from OpenGL.GL import *
from OpenGL.GLU import gluPerspective

from src.config import (
    WIDTH,
    HEIGHT,
    FPS,
    WINDOW_TITLE,
    DARK_BACKGROUND_COLOR,
)
from src.renderer import Renderer
from src.camera import Camera
from src.ui import UI
from objects.shape_manager import ShapeManager


class App:
    def __init__(self):
        pygame.init()

        self.display = (WIDTH, HEIGHT)
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption(WINDOW_TITLE)

        self.clock = pygame.time.Clock()
        self.running = True
        self.auto_rotate = True
        self.wireframe = False

        self.rotation_x = 0
        self.rotation_y = 0
        self.mouse_dragging = False
        self.last_mouse_pos = None

        self.renderer = Renderer()
        self.camera = Camera()
        self.shape_manager = ShapeManager()
        self.ui = UI(WIDTH, HEIGHT)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False

                elif event.key == K_SPACE:
                    self.auto_rotate = not self.auto_rotate

                elif event.key == K_q:
                    self.camera.zoom_in()

                elif event.key == K_e:
                    self.camera.zoom_out()

                elif event.key == K_p:
                    self.save_screenshot()

                elif event.key == K_n:
                    self.shape_manager.next_shape()

                elif event.key == K_m:
                    self.wireframe = not self.wireframe

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos

                    action = self.ui.handle_click(
                        (mouse_x, mouse_y),
                        self.auto_rotate,
                        self.shape_manager.get_shape_names()
                    )

                    if action == "toggle":
                        self.auto_rotate = not self.auto_rotate

                    elif action == "screenshot":
                        self.save_screenshot()

                    elif action == "reset":
                        self.rotation_x = 0
                        self.rotation_y = 0
                        self.camera.x = 0
                        self.camera.y = 0
                        self.camera.z = -8

                    elif isinstance(action, tuple) and action[0] == "shape":
                        self.shape_manager.set_shape(action[1])

                    else:
                        self.mouse_dragging = True
                        self.last_mouse_pos = event.pos

            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_dragging = False
                    self.last_mouse_pos = None

            elif event.type == MOUSEMOTION:
                if self.mouse_dragging:
                    x, y = event.pos
                    last_x, last_y = self.last_mouse_pos

                    dx = x - last_x
                    dy = y - last_y

                    self.rotation_y += dx * 0.5
                    self.rotation_x += dy * 0.5

                    self.last_mouse_pos = event.pos

    def handle_keyboard_input(self):
        keys = pygame.key.get_pressed()

        if keys[K_a]:
            self.camera.move_left()

        if keys[K_d]:
            self.camera.move_right()

        if keys[K_w]:
            self.camera.move_up()

        if keys[K_s]:
            self.camera.move_down()

    def update(self):
        self.handle_keyboard_input()

        if self.auto_rotate:
            self.rotation_y += 0.6
            self.rotation_x += 0.3

    def render(self):
        self.renderer.clear(DARK_BACKGROUND_COLOR)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, WIDTH / HEIGHT, 0.1, 50.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.camera.apply()
        self.renderer.draw_grid()

        glPushMatrix()
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)
        self.shape_manager.draw(self.wireframe)
        glPopMatrix()

        self.ui.draw(
            self.auto_rotate,
            self.shape_manager.get_current_shape_name(),
            self.wireframe,
            self.shape_manager.get_shape_names()
        )

        pygame.display.flip()

    def save_screenshot(self):
        os.makedirs("assets/screenshots", exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"assets/screenshots/visualizer_{timestamp}.png"

        width, height = self.display

        pixels = glReadPixels(
            0, 0, width, height,
            GL_RGB,
            GL_UNSIGNED_BYTE
        )

        image = Image.frombytes("RGB", (width, height), pixels)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image.save(filename)

        self.ui.show_notification("Screenshot saved successfully")
        print(f"Screenshot saved: {filename}")

    def update_window_title(self):
        fps = int(self.clock.get_fps())
        pygame.display.set_caption(f"{WINDOW_TITLE} | FPS: {fps}")

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.update_window_title()
            self.clock.tick(FPS)

        pygame.quit()