#!/usr/bin/env python3
import sys
import numpy as np
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass

def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()

def egg_points(N):
    tab = np.zeros((N, N, 3))

    u = np.linspace(0, 1, N)
    v = np.linspace(0, 1, N)

    for i in range(N):
        for j in range(N):
            tab[i][j][0] = (-90 * u[i]**5 + 225 * u[i]**4 - 270 * u[i]**3 + 180 * u[i]**2 - 45 * u[i]) * np.cos(np.pi * v[j])
            tab[i][j][1] = 160 * u[i] ** 4 - 320 * u[i] ** 3 + 160 * u[i] ** 2 - 5
            tab[i][j][2] = (-90 * u[i]**5 + 225 * u[i]**4 - 270 * u[i]**3 + 180 * u[i]**2 - 45 * u[i]) * np.sin(np.pi * v[j])

    return tab


def draw_egg(N):
    vertexes = egg_points(N)
    colors = np.zeros((N, N, 3))

    for i in range(N):
        for j in range(N):
            if i < N // 2:
                r_color = i / N
                g_color = j / N
                b_color = 1
            else:
                r_color = (N - 1 - i) / N
                g_color = (N - 1 - j) / N
                b_color = 1

            colors[i, j] = [r_color, g_color, b_color]

    for i in range(N - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            r_color, g_color, b_color = colors[i, j]
            glColor3f(r_color, g_color, b_color)
            glVertex3fv(vertexes[i][j])

            r_color, g_color, b_color = colors[i + 1, j]
            glColor3f(r_color, g_color, b_color)
            glVertex3fv(vertexes[i + 1][j])

        glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time*180 / 3.1415)

    axes()
    draw_egg(50)

    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

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
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
