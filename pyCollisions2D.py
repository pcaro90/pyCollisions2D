#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright (c) 2014 Pablo Caro. All Rights Reserved.
# Pablo Caro <me@pcaro.es> - https://pcaro.es/
# pyCollisions2D.py
# ----------------------------------------------------------------------

import random
import sys

try:
    import pygame
    from pygame.locals import QUIT, KEYDOWN, K_q, K_ESCAPE
except:
    print "ERROR: PyGame cannot be imported. Exitting now."
    sys.exit()

MAX_FPS = 30
SIZE = (1280, 720)

BALLS = 200


class Particle:
    def __init__(self, id=0):
        self.id = id
        self.s = [random.uniform(0, SIZE[i] - 1) for i in range(2)]
        self.v = [random.uniform(-42, 42) for i in range(2)]
        self.a = [0.0] * 2

        self.m = random.uniform(1, 256)
        # self.r = random.uniform(8, 16)
        self.r = 12

    def move(self, ms):
        for i in range(len(self.s)):
            self.v[i] += self.a[i] * (ms / 1000.0)
            self.s[i] += self.v[i] * (ms / 1000.0)

    def distance(self, p):
        d = 0.0
        for x1, x2 in zip(self.s, p.s):
            d += abs(x1 - x2) ** 2.0
        return d ** 0.5


def random_particles(n):
    particles = []
    for i in range(n):
        inserted = False
        while not inserted:
            np = Particle(i)
            for p in particles:
                if p.distance(np) < p.r + np.r:
                    break
            else:
                inserted = True
        particles.append(np)

    return particles


def dot_product(v1, v2):
    r = 0.0
    for a, b in zip(v1, v2):
        r += a * b
    return r


def scalar_product(v, n):
    return [i * n for i in v]


def normalize(v):
    m = 0.0
    for spam in v:
        m += spam ** 2.0
    m = m ** 0.5

    return [spam / m for spam in v]




def main():
    # UI things
    pygame.init()
    windowSurface = pygame.display.set_mode(SIZE, 0, 32)
    pygame.display.set_caption("Collisions 2D")

    mainClock = pygame.time.Clock()

    particles = random_particles(BALLS)

    end = False
    while not end:
        t = mainClock.tick(MAX_FPS)
        handle_events()

        ### Compute cycle ###

        # Particles collision
        for i, p1 in enumerate(particles):
            for p2 in particles[i + 1:]:
                d = p1.distance(p2)
                if (d <= p1.r + p2.r):
                    N = normalize([p1.s[0] - p2.s[0], p1.s[1] - p2.s[1]])

                    d1 = 1.1 * ((p1.r + p2.r - d) * p2.m) / (p1.m + p2.m)
                    d2 = 1.1 * ((p1.r + p2.r - d) * p1.m) / (p1.m + p2.m)

                    p1.s[0] += N[0] * d1
                    p1.s[1] += N[1] * d1

                    p2.s[0] -= N[0] * d2
                    p2.s[1] -= N[1] * d2

                    T = [-N[1], N[0]]

                    v1n = dot_product(N, p1.v)
                    v1t = dot_product(T, p1.v)

                    v2n = dot_product(N, p2.v)
                    v2t = dot_product(T, p2.v)

                    u1n = v1n
                    v1n = ((v1n * (p1.m - p2.m) + 2.0 * p2.m * v2n) / (p1.m +
                           p2.m))
                    v2n = ((v2n * (p2.m - p1.m) + 2.0 * p1.m * u1n) / (p2.m +
                           p1.m))

                    vn = scalar_product(N, v1n)
                    vt = scalar_product(T, v1t)
                    p1.v = [a + b for a, b in zip(vn, vt)]

                    vn = scalar_product(N, v2n)
                    vt = scalar_product(T, v2t)
                    p2.v = [a + b for a, b in zip(vn, vt)]

        # Bounce on edges
        for p in particles:
            for i in range(2):  # For every dimension (2)
                if p.s[i] < p.r and p.v[i] < 0:
                    p.v[i] = -p.v[i]
                elif p.s[i] + p.r > SIZE[i] and p.v[i] > 0:
                    p.v[i] = -p.v[i]

        for p in particles:
            p.move(t)

        #### Draw cycle ####
        windowSurface.fill((200, 200, 255))
        for p in particles:
            c = 256 - p.m
            pygame.draw.circle(
                windowSurface, (c, c, c), map(int, p.s), int(p.r))

        pygame.display.update()

    terminate()  # Quit PyGame and Python


def handle_events():
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        elif event.type == KEYDOWN:
            if event.key in (K_ESCAPE, K_q):
                terminate()


def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
