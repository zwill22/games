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

import math

from platformer.engine import Sprite
from platformer.objects import Player


class Enemy(Sprite):
    """
    Spawn an enemy
    """

    def __init__(self, x, y, *imgs, **kwargs):

        Sprite.__init__(self, x, y, *imgs, **kwargs)

        self.counter = 0

        self.is_falling = True
        self.health = 1

    def move(self):
        """
        Enemy movement
        """
        # TODO Remove magic numbers, make attributes
        speed = 4
        n = 20

        sign = math.copysign(1, math.sin(self.counter * math.pi / n))

        self.move_x = sign * speed
        if self.counter < 10 * n:
            self.counter += 1
        else:
            self.counter = 0

    def gravity(self, world_y, ty):
        """
        Simulate gravity on enemy
        """
        if self.is_falling:
            self.move_y += 2
            self.rect.y += self.move_y

        if self.rect.y > world_y and self.move_y >= 0:
            self.move_y = 0
            self.rect.y = world_y - ty - ty

    def update(self, player: Player, enemy_list, ground_list, plat_list, firepower):
        """
        Update sprite position and detect collisions
        """
        self.update_sprite()

        if self.hit(player):
            self.health -= 1

        fire_hit_list = self.hit_list(firepower)
        for _ in fire_hit_list:
            # TODO Add death animation
            enemy_list.remove(self)

        for ob_list in (ground_list, plat_list):
            ground_hit_list = self.hit_list(ob_list)
            for g in ground_hit_list:
                self.move_y = 0
                self.rect.bottom = g.rect.top
                self.is_falling = False
