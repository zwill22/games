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

import os

from variables import worldy, worldx
from code.engine import Sprite

from pygame.mixer import Sound


class Player(Sprite):
    """
    Spawn a player
    """

    def __init__(self, x, y, **kwargs):
        hero = ["hero-{}.png".format(i) for i in range(4)]

        Sprite.__init__(self, x, y, *hero, **kwargs)
        self.frame = 0
        self.health = 10
        self.damage = False
        self.score = 0

        self.is_jumping = True
        self.is_falling = False

    def gravity(self):
        if self.is_jumping:
            self.movey += 2

    def jump(self):
        if not self.is_jumping:
            self.is_falling = False
            self.is_jumping = True

    def update(self, enemy_list, ground_list, plat_list, loot_list,
                      tx, ty):
        """
        Update sprite position
        """
        self.update_sprite()

        if self.movex < 0 or self.movex > 0:
            self.is_jumping = True

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


class Enemy(Sprite):
    """
    Spawn an enemy
    """
    def __init__(self, x, y, *imgs, **kwargs):

        Sprite.__init__(self, x, y, *imgs, **kwargs)

        self.counter = 0

        self.is_falling = True
        self.health = 1

        # TODO Remove sound
        self.burn = Sound(os.path.join('sound', 'fire_sound_effect.mp3'))

    def move(self):
        """
        Enemy movement
        """
        # TODO Remove magic numbers
        distance = 30
        speed = 4

        if 0 <= self.counter <= distance:
            self.movex = speed
        elif distance < self.counter <= distance * 2:
            self.movex = -speed
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
        self.update_sprite()

        if self.hit(player):
            self.health -= 1
            print(self.health)

        fire_hit_list = self.hit_list(firepower)
        for fire in fire_hit_list:
            # TODO Add death animation
            enemy_list.remove(self)
            self.burn.play(1, 150)

        for ob_list in (ground_list, plat_list):
            ground_hit_list = self.hit_list(ob_list)
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

        speed = 15
        if forward:
            self.movex = speed
        else:
            self.movex = -speed
        self.movey = 0

    def update(self):
        """
        Throw physics
        """
        self.update_sprite()

        if 0 < self.rect.y < worldy and 0 < self.rect.x < worldx:
            pass
        else:
            self.kill()
            self.firing = False


Platform = Sprite
