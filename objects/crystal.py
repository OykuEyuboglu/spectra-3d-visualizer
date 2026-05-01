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
    vec3 light_dir = normalize(vec3(0.6, 0.9, 0.7));

    float diffuse = max(dot(normal, light_dir), 0.0);

    vec3 reflect_dir = reflect(-light_dir, normal);
    float specular = pow(max(dot(view_dir, reflect_dir), 0.0), 96.0);

    float fresnel = pow(1.0 - max(dot(view_dir, normal), 0.0), 2.8);

    float rainbow = sin((normal.x + normal.y + normal.z) * 8.0 + u_time * 1.8);

    vec3 base_color = vec3(0.58, 0.46, 0.86);      // soft purple
    vec3 deep_purple = vec3(0.32, 0.20, 0.55);     // shadow purple
    vec3 lavender = vec3(0.78, 0.62, 1.00);        // light purple
    vec3 pink_glow = vec3(1.00, 0.48, 0.86);       // pink reflection
    vec3 icy_blue = vec3(0.62, 0.82, 1.00);        // small cool highlight

    float shift = 0.5 + 0.5 * sin((normal.x - normal.y + normal.z) * 7.0 + u_time * 1.4);

    vec3 purple_gradient = mix(deep_purple, lavender, shift);
    vec3 reflection_color = mix(pink_glow, icy_blue, fresnel);

    vec3 color =
        purple_gradient * (0.30 + diffuse * 0.55)
        + reflection_color * fresnel * 0.85
        + vec3(1.0, 0.88, 1.0) * specular * 1.8;
    
    
    gl_FragColor = vec4(color, 0.82);
}
"""


class Crystal(BaseShape):
    def __init__(self):
        super().__init__()
        self.name = "Diamond"

        self.vertices = self.create_vertices()
        self.faces = self.create_faces()
        self.edges = self.create_edges()

        self.shader = compileProgram(
            compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
            compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
        )

    def create_vertices(self):
        vertices = []

        vertices.append((0.0, 0.9, 0.0))

        for i in range(8):
            angle = math.radians(i * 45)
            vertices.append((0.55 * math.cos(angle), 0.55, 0.55 * math.sin(angle)))

        for i in range(8):
            angle = math.radians(i * 45 + 22.5)
            vertices.append((1.25 * math.cos(angle), 0.0, 1.25 * math.sin(angle)))

        vertices.append((0.0, -1.45, 0.0))

        return vertices

    def create_faces(self):
        top = 0
        upper_start = 1
        girdle_start = 9
        bottom = 17

        faces = []

        for i in range(8):
            next_i = (i + 1) % 8

            upper_a = upper_start + i
            upper_b = upper_start + next_i

            girdle_a = girdle_start + i
            girdle_b = girdle_start + next_i

            faces.append((top, upper_a, upper_b))

            faces.append((upper_a, girdle_a, girdle_b))
            faces.append((upper_a, girdle_b, upper_b))

            faces.append((bottom, girdle_b, girdle_a))

        return faces

    def create_edges(self):
        edges = []

        for face in self.faces:
            edges.append((face[0], face[1]))
            edges.append((face[1], face[2]))
            edges.append((face[2], face[0]))

        return list(set(tuple(sorted(edge)) for edge in edges))

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
            return 0, 1, 0

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
        glColor3f(0.95, 0.98, 1.0)
        glLineWidth(1.6)

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

        for i in range(36):
            angle = math.radians(i * 10)
            radius = 1.8 + 0.15 * math.sin(time.time() * 2 + i)

            x = math.cos(angle) * radius
            y = 0.2 * math.sin(time.time() * 2 + i)
            z = math.sin(angle) * radius

            glColor4f(0.85, 0.55, 1.0, 0.55)
            glVertex3f(x, y, z)

        glEnd()

        glDisable(GL_BLEND)

    def draw(self, wireframe=False):
        self.draw_solid()
        self.draw_glow()

        if wireframe:
            self.draw_wireframe()