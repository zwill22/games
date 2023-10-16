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

from variables import ani, worldy, worldx


class Sprite(pygame.sprite.Sprite):
    """
    Generic sprite class based on pygames Sprite
    """
    def __init__(self, xloc, yloc, *images, image_dir='images', alpha=0):
        pygame.sprite.Sprite.__init__(self)

        self.images = []
        for image in images:
            img = pygame.image.load(os.path.join(image_dir, image)).convert()
            img.convert_alpha()
            img.set_colorkey(alpha)
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = xloc
        self.rect.y = yloc

    def hit_list(self, ob_list):
        return pygame.sprite.spritecollide(self, ob_list, False)

    def hit(self, pysprite) -> bool:
        return pysprite.rect.colliderect(self.rect)


class Player(Sprite):
    """
    Spawn a player
    """

    def __init__(self, x, y, **kwargs):
        hero = ["hero-{}.png".format(i) for i in range(4)]

        Sprite.__init__(self, x, y, *hero, **kwargs)
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.health = 10
        self.damage = False
        self.score = 0

        self.facing_right = True

        self.is_jumping = True
        self.is_falling = False

    def draw(self, world):
        player_list = pygame.sprite.Group()
        player_list.add(self)
        player_list.draw(world)

    def gravity(self, ty):
        if self.is_jumping:
            self.movey += 2

    def control(self, x, y):
        """
        Control player movement
        """
        self.movex += x
        self.movey += y

    def jump(self):
        if not self.is_jumping:
            self.is_falling = False
            self.is_jumping = True

    def stop(self):
        """
        Stop player movement
        """
        self.movex = 0
        self.movey = 0

    def update(self, enemy_list, ground_list, plat_list, loot_list, tx, ty):
        """
        Update sprite position
        """

        if self.movex < 0 or self.movex > 0:
            self.is_jumping = True
            self.frame += 1
            if self.frame > 3 * ani:
                self.frame = 0

        if self.movex < 0:
            self.image = pygame.transform.flip(
                self.images[self.frame//ani], True, False
            )

        if self.movex > 0:
            self.image = self.images[self.frame//ani]

        enemy_hit_list = self.hit_list(enemy_list)
        if not self.damage:
            for enemy in enemy_list:
                if not self.rect.contains(enemy):
                    self.damage = self.rect.colliderect(enemy)
        if self.damage:
            idx = self.rect.collidelist(enemy_hit_list)
            if idx == -1:
                self.damage = 0
                self.health -= 1

        ground_hit_list = self.hit_list(ground_list)
        for g in ground_hit_list:
            self.movey = 0
            self.rect.bottom = g.rect.top
            self.is_jumping = False

        loot_hit_list = self.hit_list(loot_list)
        for loot in loot_hit_list:
            loot_list.remove(loot)
            self.score += 1

        plat_hit_list = self.hit_list(plat_list)
        for p in plat_hit_list:
            self.is_jumping = False
            self.movey = 0

            # approach from below
            if self.rect.bottom < p.rect.bottom:
                self.rect.bottom = p.rect.top
            else:
                self.movey += 2

        # Fall off the world
        if self.rect.y > worldy:
            self.health -= 1
            self.rect.x = tx
            self.rect.y = ty

        if self.is_jumping and not self.is_falling:
            self.is_falling = True
            self.movey -= 24

        self.rect.x += self.movex
        self.rect.y += self.movey


class Enemy(Sprite):
    """
    Spawn an enemy
    """
    def __init__(self, x, y, *imgs, **kwargs):

        Sprite.__init__(self, x, y, *imgs, **kwargs)

        self.counter = 0
        self.frame = 0

        self.movey = 0
        self.is_falling = True

        self.forward = True
        self.health = 1

        self.burn = pygame.mixer.Sound(
            os.path.join('sound', 'fire_sound_effect.mp3'))

    def move(self):
        """
        Enemy movement
        """
        # TODO Remove magic numbers
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

    def update(self, player: Player, enemy_list, ground_list, plat_list,
               firepower):
        """
        Update sprite position and detect collisions
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

        if self.hit(player):
            self.health -= 1
            print(self.health)

        fire_hit_list = pygame.sprite.spritecollide(self, firepower, False)
        for fire in fire_hit_list:
            # TODO Add death animation
            enemy_list.remove(self)
            self.burn.play(1, 150)

        for ob_list in (ground_list, plat_list):
            ground_hit_list = pygame.sprite.spritecollide(
                self, ob_list, False)
            for g in ground_hit_list:
                self.movey = 0
                self.rect.bottom = g.rect.top
                self.is_falling = False


class Throwable(Sprite):
    """
    Spawn a throwable object
    """
    def __init__(self, x, y, *images, throw=False, forward=True, **kwargs):
        Sprite.__init__(self, x, y, *images, **kwargs)

        self.firing = throw
        self.forward = forward

    def update(self):
        """
        Throw physics
        """
        if 0 < self.rect.y < worldy and 0 < self.rect.x < worldx:
            if self.forward:
                self.rect.x += 15
            else:
                self.rect.x -= 15
            self.rect.y += 0
        else:
            self.kill()
            self.firing = False


Platform = Sprite
