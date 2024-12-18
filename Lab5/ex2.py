#!/usr/bin/env python3
import sys
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

viewer = [0.0, 0.0, 10.0]
theta = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0

show_wall = [True, True, True, True]  # Kontrola wyświetlania ścian

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    image = Image.open("/Users/rafalzalecki/PycharmProjects/GrafikaKomputerowa/Lab5/tekstura.tga")
    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, image.size[0], image.size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, image.tobytes("raw", "RGB", 0, -1)
    )


def render_pyramid():
    global show_wall

    # Wierzchołki ostrosłupa
    base_vertices = [
        [-5.0, -5.0, 0.0],
        [5.0, -5.0, 0.0],
        [5.0, 5.0, 0.0],
        [-5.0, 5.0, 0.0]
    ]
    top_vertex = [0.0, 0.0, 5.0]

    # Tekstura dla podstawy
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3fv(base_vertices[0])
    glTexCoord2f(1.0, 0.0)
    glVertex3fv(base_vertices[1])
    glTexCoord2f(1.0, 1.0)
    glVertex3fv(base_vertices[2])
    glTexCoord2f(0.0, 1.0)
    glVertex3fv(base_vertices[3])
    glEnd()

    # Tekstura dla ścian bocznych
    glBegin(GL_TRIANGLES)
    walls = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0)
    ]
    # Nowe współrzędne tekstury dla ćwiartek
    texture_coords = [
        (0.5, 1.0),  # Wierzchołek górny (środek góry tekstury)
        (0.0, 0.5),  # Lewy dolny - ćwiartka
        (0.5, 0.5),  # Prawy dolny - ćwiartka
        (1.0, 0.5),  # Prawy górny - ćwiartka
        (0.5, 0.0),  # Lewy górny - ćwiartka
    ]

    # Zmiana pętli rysującej ściany ostrosłupa
    for i, (start, end) in enumerate(walls):
        if show_wall[i]:
            glBegin(GL_TRIANGLES)
            # Wierzchołek górny ostrosłupa
            glTexCoord2f(0.5, 1.0)  # Stałe przypisanie środka góry tekstury
            glVertex3f(*top_vertex)

            # Wierzchołki podstawy - mapowanie ćwiartek tekstury
            glTexCoord2f(texture_coords[start][0], texture_coords[start][1])
            glVertex3f(*base_vertices[start])

            glTexCoord2f(texture_coords[end][0], texture_coords[end][1])
            glVertex3f(*base_vertices[end])
            glEnd()

    glEnd()


def render(time):
    global theta

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)
    render_pyramid()
    glFlush()


def keyboard_key_callback(window, key, scancode, action, mods):
    global show_wall

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key in [GLFW_KEY_1, GLFW_KEY_2, GLFW_KEY_3, GLFW_KEY_4] and action == GLFW_PRESS:
        index = key - GLFW_KEY_1
        show_wall[index] = not show_wall[index]


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    glfwTerminate()


if __name__ == '__main__':
    main()
