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

from objects import Platform, Enemy
from code.engine import SpriteList


def invalid_level(lvl):
    ValueError("Invalid level: {}".format(lvl))


def ground(lvl, gloc, world_y, ty) -> SpriteList:
    ground_list = SpriteList()

    if lvl == 1:
        for g in gloc:
            gr = Platform(g, world_y - ty, 'tile-ground.png')
            ground_list.add(gr)
    else:
        invalid_level(lvl)

    return ground_list


def platform(lvl, tx, ty, world_y) -> SpriteList:
    plat_list = SpriteList()
    plat_loc = []
    if lvl == 1:
        plat_loc.append((300, world_y - ty - 256, 4))
        plat_loc.append((200, world_y - ty - 128, 3))
        plat_loc.append((500, world_y - ty - 128, 4))
        for pl in plat_loc:
            for j in range(pl[2] + 1):
                plat = Platform((pl[0]+(j*tx)), pl[1], 'tile.png')
                plat_list.add(plat)
    else:
        invalid_level(lvl)

    return plat_list


def loot(lvl, tx, ty) -> SpriteList:
    loot_list = SpriteList()
    if lvl == 1:
        lot = Platform(tx*8, ty*7.5, 'loot_1.png')
        loot_list.add(lot)
    else:
        invalid_level(lvl)

    return loot_list


def bad(lvl, enemy_loc) -> SpriteList:
    enemy_list = SpriteList()

    if lvl == 1:
        images = ["enemy-{}.png".format(i) for i in range(4)]

        enemy = Enemy(enemy_loc[0], enemy_loc[1], *images)
        enemy_list.add(enemy)
    else:
        invalid_level(lvl)

    return enemy_list
