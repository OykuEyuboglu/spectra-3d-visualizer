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
    vec3 light_dir = normalize(vec3(0.4, 0.9, 0.7));

    float diffuse = max(dot(normal, light_dir), 0.0);

    vec3 reflect_dir = reflect(-light_dir, normal);
    float specular = pow(max(dot(view_dir, reflect_dir), 0.0), 96.0);

    float fresnel = pow(1.0 - max(dot(view_dir, normal), 0.0), 2.0);
    float pulse = 0.5 + 0.5 * sin(u_time * 2.0);

    vec3 deep_gold = vec3(0.95, 0.48, 0.05);
    vec3 gold = vec3(1.00, 0.72, 0.12);
    vec3 bright_yellow = vec3(1.00, 0.92, 0.35);
    vec3 cream = vec3(1.00, 0.96, 0.70);

    float shift = 0.5 + 0.5 * sin((normal.x + normal.y) * 5.0 + u_time);

    vec3 gradient = mix(gold, bright_yellow, shift);
    vec3 edge_glow = mix(cream, bright_yellow, pulse);

    vec3 color =
        gradient * (0.38 + diffuse * 0.62)
        + edge_glow * fresnel * 0.85
        + vec3(1.0, 0.95, 0.70) * specular * 1.8;

    gl_FragColor = vec4(color, 0.96);
}
"""


class Star(BaseShape):
    def __init__(self):
        super().__init__()
        self.name = "Star"

        self.outer_radius = 1.35
        self.inner_radius = 0.58

        # Şişkinlik buradan geliyor
        self.front_depth = 0.45
        self.back_depth = -0.45
        self.side_depth = 0.0

        self.ring_vertices = self.generate_ring_vertices(self.side_depth)

        # index 0 front center, index 1 back center
        self.vertices = [
            (0, 0, self.front_depth),
            (0, 0, self.back_depth),
        ] + self.ring_vertices

        self.faces = self.create_faces()
        self.edges = self.create_edges()

        self.shader = compileProgram(
            compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
            compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
        )

    def generate_ring_vertices(self, z):
        vertices = []

        for i in range(10):
            angle = math.radians(90 + i * 36)
            radius = self.outer_radius if i % 2 == 0 else self.inner_radius

            x = math.cos(angle) * radius
            y = math.sin(angle) * radius

            vertices.append((x, y, z))

        return vertices

    def create_faces(self):
        faces = []

        front_center = 0
        back_center = 1
        ring_start = 2

        # Front bulged triangular facets
        for i in range(10):
            a = ring_start + i
            b = ring_start + ((i + 1) % 10)
            faces.append((front_center, a, b))

        # Back bulged triangular facets
        for i in range(10):
            a = ring_start + i
            b = ring_start + ((i + 1) % 10)
            faces.append((back_center, b, a))

        return faces

    def create_edges(self):
        edges = []
        ring_start = 2

        for i in range(10):
            a = ring_start + i
            b = ring_start + ((i + 1) % 10)

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
        glColor3f(1.0, 0.92, 0.45)
        glLineWidth(1.7)

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

        for i in range(32):
            angle = math.radians(i * 360 / 32)
            radius = 1.65 + 0.12 * math.sin(time.time() * 3 + i)

            x = math.cos(angle) * radius
            y = math.sin(angle) * radius
            z = 0.15 * math.sin(time.time() * 2 + i)

            glColor4f(1.0, 0.85, 0.22, 0.45)
            glVertex3f(x, y, z)

        glEnd()

        glDisable(GL_BLEND)

    def draw(self, wireframe=False):
        self.draw_solid()
        self.draw_glow()

        if wireframe:
            self.draw_wireframe()