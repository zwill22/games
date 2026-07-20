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

from platformer.engine import Sprite

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

