#!/usr/bin/env python3
# by Zack M. Williams

# # GPLv3
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygame
import os

from variables import ani


class Player(pygame.sprite.Sprite):
    """
    Spawn a player
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.health = 10

        self.images = []
        for i in range(4):
            img = pygame.image.load(
                os.path.join('images', 'hero-{}.png'.format(i))
            ).convert()
            img.convert_alpha()
            img.set_colorkey(0)
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

    def control(self, x, y):
        """
        Control player movement
        """
        self.movex += x
        self.movey += y

    def stop(self):
        """
        Stop player movement
        """
        self.movex = 0
        self.movey = 0

    def update(self, enemy_list):
        """
        Update sprite position
        """
        self.rect.x += self.movex
        self.rect.y += self.movey

        if self.movex < 0 or self.movex > 0:
            self.frame += 1
            if self.frame > 3 * ani:
                self.frame = 0

        if self.movex < 0:
            self.image = pygame.transform.flip(
                self.images[self.frame//ani], True, False
            )

        if self.movex > 0:
            self.image = self.images[self.frame//ani]

        hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        for enemy in hit_list:
            self.health -= 1
        print("Player health: {}".format(self.health))


class Enemy(pygame.sprite.Sprite):
    """
    Spawn an enemy
    """
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)

        self.images = []
        for i in range(4):
            im = pygame.image.load(
                os.path.join('images', '{}-{}.png'.format(img, i))
            ).convert()
            im.convert_alpha()
            im.set_colorkey(0)
            self.images.append(im)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.counter = 0

    def move(self):
        """
        Enemy movement
        """
        distance = 50
        speed = 6

        if 0 <= self.counter < distance:
            self.rect.x += speed
        elif distance <= self.counter <= distance * 2:
            self.rect.x -= speed
        else:
            self.counter = 0

        self.counter += 1


class Platform(pygame.sprite.Sprite):

    def __init__(self, xloc, yloc, imgw, imgh, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images', img)).convert()
        self.image.convert_alpha()
        self.image.set_colorkey(0)
        self.rect = self.image.get_rect()
        self.rect.x = xloc
        self.rect.y = yloc
