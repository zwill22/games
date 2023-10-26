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

from code.engine import Sprite
from code.objects import Player

from pygame.mixer import Sound


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
        # TODO Remove magic numbers, make attributes
        distance = 30
        speed = 4

        if 0 <= self.counter <= distance:
            self.move_x = speed
        elif distance < self.counter <= distance * 2:
            self.move_x = -speed
        else:
            self.counter = 0

        self.counter += 1

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
                self.move_y = 0
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
            self.move_x = speed
        else:
            self.move_x = -speed
        self.move_y = 0

    def update(self, world_x, world_y):
        """
        Throw physics
        """
        self.update_sprite()

        if 0 < self.rect.y < world_y and 0 < self.rect.x < world_x:
            pass
        else:
            self.kill()
            self.firing = False


Platform = Sprite
