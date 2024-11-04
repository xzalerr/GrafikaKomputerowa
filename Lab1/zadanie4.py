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


def sierpinski_carpet(x, y, width, height, depth):
    if depth == 0:
        glColor3f(0.0, 0.0, 0.25)
        draw_rectangle(x, y, width, height)
    else:
        glColor3f(0.0, 0.0, 0.25)
        draw_rectangle(x, y, width, height)

        glColor3f(0.5, 0, 0)
        draw_rectangle(x, y, width/3, height/3)

        small_w, small_h = width/3, height/3
        for small_x in [-small_w, 0, small_w]:
            for small_y in [-small_h, 0, small_h]:
                if small_x != 0 or small_y != 0:
                    sierpinski_carpet(x+small_x, y+small_y, small_w, small_h, depth-1)


def render(time, depth):
    glClear(GL_COLOR_BUFFER_BIT)
    sierpinski_carpet(0, 0, 180, 180, depth)
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
    depth = 4
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), depth)
        glfwSwapBuffers(window)
        glfwPollEvents()

    shutdown()
    glfwTerminate()


if __name__ == '__main__':
    main()
