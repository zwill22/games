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

from platformer.objects import Platform, Enemy
from platformer.engine import SpriteList
from platformer.objects.loot import Loot


def invalid_level(lvl):
    raise ValueError("Invalid level: {}".format(lvl))


def ground(lvl, tx, ty, world_y) -> SpriteList:
    ground_list = SpriteList()

    gloc = []

    if lvl == 1:
        gloc = [index for index in range(-6, 5)]
        gloc = [*gloc, *[index for index in range(22, 28)]]
    else:
        invalid_level(lvl)

    for g in gloc:
        gr = Platform(g * tx, world_y - ty, "tile-ground.png")
        ground_list.add(gr)

    return ground_list


def platform(lvl, tx, ty, world_y) -> SpriteList:
    plat_list = SpriteList()
    platforms = []
    if lvl == 1:
        platforms = [(5, 3, 3), (8, 5, 4), (12, 7, 3), (15, 5, 4), (19, 3, 3)]
    else:
        invalid_level(lvl)

    for pl in platforms:
        for j in range(pl[2]):
            plat = Platform((pl[0] + j) * tx, world_y - pl[1] * ty, "tile.png")
            plat_list.add(plat)

    return plat_list


def loot(lvl, tx, ty, world_y) -> SpriteList:
    loot_list = SpriteList()

    loots = []
    final_loot = (0, 0)
    if lvl == 1:
        loots = [(6, 4), (13, 8), (20, 4)]
        final_loot = (26, 2)
    else:
        invalid_level(lvl)

    images = [f"loot-{i}.png" for i in [1, 2, 3, 2]]
    for gem in loots:
        loot_gem = Loot(gem[0] * tx, world_y - gem[1] * ty, *images)
        loot_list.add(loot_gem)

    loot_list.add(
        Loot(final_loot[0] * tx, world_y - final_loot[1] * ty, "final-loot.png")
    )

    return loot_list


def enemies(lvl, tx, ty, world_y) -> SpriteList:
    enemy_list = SpriteList()

    images = []
    positions = []

    if lvl == 1:
        images = [f"enemy-{i}.png" for i in [0, 1, 2, 1]]

        positions = [(9, 5), (16, 5)]
    else:
        invalid_level(lvl)

    for position in positions:
        enemy = Enemy(position[0] * tx, world_y - position[1] * ty, *images)
        enemy_list.add(enemy)

    return enemy_list
