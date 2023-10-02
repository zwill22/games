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

from variables import worldy
from objects import Platform, Enemy


def invalid_level(lvl):
    ValueError("Invalid level: {}".format(lvl))

# def ground(self, lvl, x, y, w, h):
    #     ground_list = pygame.sprite.Group()
    #     if lvl == 1:
    #         gr = Platform(x, y, w, h, 'block-ground.png')
    #         ground_list.add(gr)
    #     else:
    #         self.invalid_level(lvl)
    #
    #     return ground_list


def ground(lvl, gloc, tx, ty):
    ground_list = pygame.sprite.Group()
    i = 0
    if lvl == 1:
        for g in gloc:
            gr = Platform(g, worldy - ty, tx, ty, 'tile-ground.png')
            ground_list.add(gr)
    else:
        invalid_level()

    return ground_list

# def platform(lvl):
#     plat_list = pygame.sprite.Group()
#     if lvl == 1:
#         plat = Platform(200, worldy - 97 - 128, 285, 67,
#                         'block-big.png')
#         plat_list.add(plat)
#         plat = Platform(500, worldy - 97 - 320, 197, 54,
#                         'block-small.png')
#         plat_list.add(plat)
#     else:
#         invalid_level(lvl)
#
#     return plat_list


def platform(lvl, tx, ty):
    plat_list = pygame.sprite.Group()
    ploc = []
    if lvl == 1:
        ploc.append((300, worldy-ty-256, 4))
        ploc.append((200, worldy-ty-128, 3))
        ploc.append((500, worldy-ty-128, 4))
        for pl in ploc:
            for j in range(pl[2] + 1):
                plat = Platform((pl[0]+(j*tx)), pl[1], tx, ty, 'tile.png')
                plat_list.add(plat)
    else:
        invalid_level(lvl)

    return plat_list


def bad(lvl, eloc):
    enemy_list = pygame.sprite.Group()

    if lvl == 1:
        enemy = Enemy(eloc[0], eloc[1], 'enemy')
        enemy_list.add(enemy)
    else:
        invalid_level(lvl)

    return enemy_list