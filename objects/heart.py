import math
import time
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from objects.base_shape import BaseShape


VERTEX_SHADER = """
varying vec3 v_normal;
varying vec3 v_position;

void main()
{
    v_normal = normalize(gl_NormalMatrix * gl_Normal);
    v_position = vec3(gl_ModelViewMatrix * gl_Vertex);
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}
"""


FRAGMENT_SHADER = """
varying vec3 v_normal;
varying vec3 v_position;

uniform float u_time;

void main()
{
    vec3 normal = normalize(v_normal);
    vec3 view_dir = normalize(-v_position);
    vec3 light_dir = normalize(vec3(0.45, 0.85, 0.8));

    float diffuse = max(dot(normal, light_dir), 0.0);

    vec3 reflect_dir = reflect(-light_dir, normal);
    float specular = pow(max(dot(view_dir, reflect_dir), 0.0), 110.0);

    float fresnel = pow(1.0 - max(dot(view_dir, normal), 0.0), 2.0);
    float pulse = 0.5 + 0.5 * sin(u_time * 2.2);

    vec3 deep_rose = vec3(0.68, 0.05, 0.25);
    vec3 rose = vec3(1.00, 0.28, 0.55);
    vec3 candy_pink = vec3(1.00, 0.48, 0.72);
    vec3 soft_highlight = vec3(1.00, 0.82, 0.92);
    vec3 purple_glow = vec3(0.72, 0.35, 1.00);

    float shift = 0.5 + 0.5 * sin((normal.x + normal.y) * 5.8 + u_time);

    vec3 gradient = mix(deep_rose, candy_pink, shift);
    vec3 glow = mix(purple_glow, soft_highlight, pulse);

    vec3 color =
        gradient * (0.36 + diffuse * 0.64)
        + glow * fresnel * 0.95
        + vec3(1.0, 0.82, 0.92) * specular * 1.9;

    gl_FragColor = vec4(color, 0.97);
}
"""


class Heart(BaseShape):
    def __init__(self):
        super().__init__()
        self.name = "Heart"

        self.scale = 0.092
        self.front_depth = 0.72
        self.back_depth = -0.72
        self.side_depth = 0.0
        self.point_count = 120

        self.ring_vertices = self.generate_ring_vertices(self.side_depth)

        self.vertices = [
            (0, 0.03, self.front_depth),
            (0, 0.03, self.back_depth),
        ] + self.ring_vertices

        self.faces = self.create_faces()
        self.edges = self.create_edges()

        self.shader = compileProgram(
            compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
            compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
        )

    def generate_ring_vertices(self, z):
        vertices = []

        for i in range(self.point_count):
            t = 2 * math.pi * i / self.point_count

            x = 16 * math.sin(t) ** 3
            y = (
                13 * math.cos(t)
                - 5 * math.cos(2 * t)
                - 2 * math.cos(3 * t)
                - math.cos(4 * t)
            )

            vertices.append((x * self.scale, y * self.scale - 0.18, z))

        return vertices

    def create_faces(self):
        faces = []
        ring_start = 2

        for i in range(self.point_count):
            a = ring_start + i
            b = ring_start + ((i + 1) % self.point_count)
            faces.append((0, a, b))

        for i in range(self.point_count):
            a = ring_start + i
            b = ring_start + ((i + 1) % self.point_count)
            faces.append((1, b, a))

        return faces

    def create_edges(self):
        edges = []
        ring_start = 2

        for i in range(self.point_count):
            a = ring_start + i
            b = ring_start + ((i + 1) % self.point_count)

            edges.append((a, b))
            edges.append((0, a))
            edges.append((1, a))

        return edges

    def calculate_normal(self, face):
        v1 = self.vertices[face[0]]
        v2 = self.vertices[face[1]]
        v3 = self.vertices[face[2]]

        ax, ay, az = v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2]
        bx, by, bz = v3[0] - v1[0], v3[1] - v1[1], v3[2] - v1[2]

        nx = ay * bz - az * by
        ny = az * bx - ax * bz
        nz = ax * by - ay * bx

        length = math.sqrt(nx * nx + ny * ny + nz * nz)

        if length == 0:
            return 0, 0, 1

        return nx / length, ny / length, nz / length

    def draw_solid(self):
        glUseProgram(self.shader)

        time_location = glGetUniformLocation(self.shader, "u_time")
        glUniform1f(time_location, time.time())

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glBegin(GL_TRIANGLES)

        for face in self.faces:
            normal = self.calculate_normal(face)
            glNormal3fv(normal)

            for vertex_index in face:
                glVertex3fv(self.vertices[vertex_index])

        glEnd()

        glDisable(GL_BLEND)
        glUseProgram(0)

    def draw_wireframe(self):
        glColor3f(1.0, 0.72, 0.88)
        glLineWidth(1.4)

        glBegin(GL_LINES)

        for edge in self.edges:
            glVertex3fv(self.vertices[edge[0]])
            glVertex3fv(self.vertices[edge[1]])

        glEnd()

    def draw_glow(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)

        glPointSize(4)
        glBegin(GL_POINTS)

        for i in range(44):
            angle = math.radians(i * 360 / 44)
            radius = 1.65 + 0.13 * math.sin(time.time() * 3 + i)

            x = math.cos(angle) * radius
            y = math.sin(angle) * radius * 0.85
            z = 0.18 * math.sin(time.time() * 2 + i)

            glColor4f(1.0, 0.36, 0.70, 0.46)
            glVertex3f(x, y, z)

        glEnd()

        glDisable(GL_BLEND)

    def draw(self, wireframe=False):
        self.draw_solid()
        self.draw_glow()

        if wireframe:
            self.draw_wireframe()