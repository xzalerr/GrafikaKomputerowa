#!/usr/bin/env python3
import sys
import random

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(1.0, 1.0, 1.0, 1.0)  # Ustawiamy kolor tła na biały


def shutdown():
    pass

def draw_rectangle(x, y, a, b):
    glBegin(GL_TRIANGLES)
    glVertex2f(x - a / 2, y - b / 2)
    glVertex2f(x + a / 2, y - b / 2)
    glVertex2f(x + a / 2, y + b / 2)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(x + a / 2, y + b / 2)
    glVertex2f(x - a / 2, y + b / 2)
    glVertex2f(x - a / 2, y - b / 2)
    glEnd()

    glFlush()

def draw_triangle(x1, y1, x2, y2, x3, y3):
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    glEnd()

    glFlush()


def sierpinski_triangle(p1, p2, p3, depth):
    if depth == 0:
        glColor3f(0.0, 1.0, 0.5)
        draw_triangle(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1])
    else:
        mid12 = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]
        mid23 = [(p2[0] + p3[0]) / 2, (p2[1] + p3[1]) / 2]
        mid31 = [(p3[0] + p1[0]) / 2, (p3[1] + p1[1]) / 2]

        sierpinski_triangle(p1, mid12, mid31, depth - 1)
        sierpinski_triangle(mid12, p2, mid23, depth - 1)
        sierpinski_triangle(mid31, mid23, p3, depth - 1)

def render(time, depth):
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.2, 0.3, 0.6)
    draw_rectangle(0, 0, 200, 200)
    sierpinski_triangle([-100, -75], [100, -75], [0, 100], depth)
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
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

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
    depth = 7
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), depth)
        glfwSwapBuffers(window)
        glfwPollEvents()

    shutdown()
    glfwTerminate()


if __name__ == '__main__':
    main()
