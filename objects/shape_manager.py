from objects.cube import Cube
from objects.pyramid import Pyramid
from objects.octahedron import Octahedron
from objects.rectangular_prism import RectangularPrism
from objects.star import Star
from objects.heart import Heart
from objects.crystal import Crystal


class ShapeManager:
    def __init__(self):
        self.shapes = [
            Cube(),
            Pyramid(),
            Octahedron(),
            RectangularPrism(),
            Star(),
            Heart(),
            Crystal(),
        ]

        self.current_index = 0

    @property
    def current_shape(self):
        return self.shapes[self.current_index]

    def next_shape(self):
        self.current_index = (self.current_index + 1) % len(self.shapes)

    def set_shape(self, index):
        if 0 <= index < len(self.shapes):
            self.current_index = index

    def draw(self, wireframe=False):
        self.current_shape.draw(wireframe)

    def get_current_shape_name(self):
        return self.current_shape.name

    def get_shape_names(self):
        return [shape.name for shape in self.shapes]