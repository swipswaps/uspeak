#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from pygame import camera
from pygame.constants import QUIT, K_ESCAPE, KEYDOWN
import numpy as np


class Capture(object):
    def __init__(self):
        camera.init()
        self.size = (640, 480, )
        # create a display surface. standard pygame stuff
        self.display = pygame.display.set_mode(self.size, 0)

        # this is the same as what we saw before
        self.clist = pygame.camera.list_cameras()
        if not self.clist:
            raise ValueError("Sorry, no cameras detected.")
        self.cam = pygame.camera.Camera(self.clist[0], self.size)
        self.cam.start()

        # create a surface to capture to.  for performance purposes
        # bit depth is the same as that of the display surface.
        self.snapshot = pygame.surface.Surface(self.size, 0, self.display)
        self.thresholded = pygame.surface.Surface(self.size, 0, self.display)
        self.previous_pixels = None

    def get_and_flip(self):
        # if you don't want to tie the framerate to the camera, you can check
        # if the camera has an image ready.  note that while this works
        # on most cameras, some will never return true.
        if self.cam.query_image():
            self.snapshot = self.cam.get_image(self.snapshot)
            pixels = pygame.surfarray.array3d(self.snapshot).astype(np.int)  # np.int to make it signed
            if self.previous_pixels is not None:
                # Get image difference
                p = np.subtract(pixels, self.previous_pixels)
                # Reset all pixels below threshold
                threshold = 30
                bool_matrix = np.logical_and(p < threshold, p > -threshold)
                p[bool_matrix] = 0
                # p[np.invert(bool_matrix)] = 200
                # Show differential image
                self.snapshot = pygame.surfarray.make_surface(p)
            self.previous_pixels = pixels

        # blit it to the display surface.  simple!
        self.display.blit(self.snapshot, (0,0))
        pygame.display.flip()

    def main(self):
        going = True
        while going:
            events = pygame.event.get()
            for e in events:
                if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                    # close the camera safely
                    self.cam.stop()
                    going = False

            self.get_and_flip()


Capture().main()
