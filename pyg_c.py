import ctypes

import pygame
import numpy

#NOTE that the 2d numpy array is x-major, meaning an array of columns

WIDTH = 320
HEIGHT = 240

fps_framecount = 0
fps_last_start = 0
fps_rate = 0.0

c_drawer = None
r_surf = None
r_array = None
do_quit = 0

def refreshScreen():
    global fps_framecount
    global fps_last_start
    global fps_rate

    # clear
    c_drawer.clear(0)

    # draw some points
    c_drawer.setPixel(0, 255)
    c_drawer.setPixel(239, 255)
    c_drawer.setPixel(WIDTH * HEIGHT - HEIGHT, 255)
    c_drawer.setPixel(WIDTH * HEIGHT - 1, 255)

    # throw some lines on the buffer
    for i in xrange(80):
        c_drawer.drawLine(10, i * 3, 10 + i * 3, HEIGHT - 10, i)

    # update screen
    pygame.surfarray.blit_array(r_surf, r_array)
    pygame.display.flip()

    # calc framerate
    fps_framecount += 1
    now = pygame.time.get_ticks()
    if (now - fps_last_start) > 250:
        fps_rate = fps_framecount / ((now - fps_last_start) / 1000.0)
        fps_last_start = now
        fps_framecount = 0


# setup
c_drawer = ctypes.cdll.LoadLibrary("./c_drawer.so")

pygame.init()
pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF, 8)

r_surf = pygame.display.get_surface()
pygame.surfarray.use_arraytype("numpy")
r_array = pygame.surfarray.array2d(r_surf)

c_drawer.setup(r_array.ctypes.data_as(ctypes.c_void_p), WIDTH, HEIGHT)

# loop
while not do_quit:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            do_quit = 1
        elif ev.type == pygame.KEYUP:
            if ev.key == pygame.K_ESCAPE:
                do_quit = 1
            elif ev.key == ord("f"):
                print fps_rate

    refreshScreen()

# shutdown
pygame.quit()
