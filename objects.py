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

from variables import ani, worldy


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

        self.is_jumping = True
        self.is_falling = False

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

    def gravity(self, ty):
        if self.is_jumping:
            self.movey += 2

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

    def update(self, enemy_list, ground_list, tx, ty):
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

        ground_hit_list = pygame.sprite.spritecollide(
            self, ground_list, False)
        for g in ground_hit_list:
            self.movey = 0
            self.rect.bottom = g.rect.top
            self.is_jumping = False

        # Fall off the world
        if self.rect.y > worldy:
            self.health -= 1
            print(self.health)
            self.rect.x = tx
            self.rect.y = ty


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
        self.frame = 0

        self.movey = 0
        self.is_falling = True

        self.forward = True
        self.health = 1

    def move(self):
        """
        Enemy movement
        """
        distance = 30
        speed = 4

        if 0 <= self.counter <= distance:
            self.rect.x += speed
            self.forward = True
        elif distance < self.counter <= distance * 2:
            self.rect.x -= speed
            self.forward = False
        else:
            self.counter = 0

        self.counter += 1

    def gravity(self, ty):
        """
        Simulate gravity on enemy
        """
        if self.is_falling:
            self.movey += 2
            self.rect.y += self.movey

        if self.rect.y > worldy and self.movey >= 0:
            self.movey = 0
            self.rect.y = worldy - ty - ty

    def update(self, player_list, ground_list, plat_list):
        """
        Update sprite position
        """
        self.frame += 1
        if self.frame > 3 * ani:
            self.frame = 0

        if self.forward:
            self.image = self.images[self.frame // ani]
        else:
            self.image = pygame.transform.flip(
                self.images[self.frame//ani], True, False
            )

        hit_list = pygame.sprite.spritecollide(self, player_list, False)
        for player in hit_list:
            self.health -= 1

        for ob_list in (ground_list, plat_list):
            ground_hit_list = pygame.sprite.spritecollide(
            self, ob_list, False)
            for g in ground_hit_list:
                self.movey = 0
                self.rect.bottom = g.rect.top
                self.is_falling = False


class Platform(pygame.sprite.Sprite):

    def __init__(self, xloc, yloc, imgw, imgh, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images', img)).convert()
        self.image.convert_alpha()
        self.image.set_colorkey(0)
        self.rect = self.image.get_rect()
        self.rect.x = xloc
        self.rect.y = yloc
