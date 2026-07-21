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

from platformer.engine.sprite import Sprite
from platformer.objects import Platform, Enemy
from platformer.engine import SpriteList
from platformer.objects.loot import Loot


def invalid_level(lvl):
    if lvl > 0:
        raise ValueError(f"Level not implemented: {lvl}")
    else:
        raise TypeError(f"Invalid level: {lvl}")


def get_gloc(lvl):
    gloc = []

    if lvl == 1:
        gloc = [index for index in range(-6, 5)]
        gloc = [*gloc, *[index for index in range(22, 28)]]
    else:
        invalid_level(lvl)

    return gloc


def ground(lvl, tx, ty, world_y) -> SpriteList:
    ground_list = SpriteList()

    gloc = get_gloc(lvl)

    for g in gloc:
        gr = Platform(g * tx, world_y - ty, "ground.png")

        ground_list.add(gr)

    return ground_list


def underground(lvl, tx, ty, world_y) -> SpriteList:
    underground_list = SpriteList()

    gloc = get_gloc(lvl)

    for g in gloc:
        h = world_y // ty
        for i in range(6 * h):
            underground = Sprite(g * tx, world_y + i * ty, "underground.png")
            underground_list.add(underground)

    return underground_list


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
    if lvl == 1:
        loots = [(6, 4), (13, 8), (20, 4), (25, 2, "final")]
    else:
        invalid_level(lvl)

    images = {
        "basic": [f"loot-{i}.png" for i in [0, 1, 2, 1]],
        "final": [f"final-{i}.png" for i in [0, 1, 2, 1]],
    }
    for gem in loots:
        kind = gem[2] if len(gem) == 3 else "basic"
        loot_gem = Loot(gem[0] * tx, world_y - gem[1] * ty, *images[kind], kind=kind)
        loot_list.add(loot_gem)

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
