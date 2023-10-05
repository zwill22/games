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
import sys

import level
from variables import worldx, worldy, fps, forwardx, backwardx
from objects import Player


def main():
    go = True

    """
    Setup
    """
    clock = pygame.time.Clock()
    pygame.init()

    world = pygame.display.set_mode([worldx, worldy])
    backdrop = pygame.image.load('images/stage.png')
    backdropbox = world.get_rect()

    gloc = []
    tx = 64
    ty = 64

    i = 0
    while i < (worldx/tx)+tx:
        gloc.append(i*tx)
        i += 1

    player = Player()
    player.rect.x = 0
    player.rect.y = 0
    player_list = pygame.sprite.Group()
    player_list.add(player)
    steps = 10

    ground_list = level.ground(1, gloc, tx, ty)
    plat_list = level.platform(1, tx, ty)

    eloc = [plat_list.sprites()[1].rect.x,
            plat_list.sprites()[1].rect.y - ty]
    enemy_list = level.bad(1, eloc)

    loot_list = level.loot(1, tx, ty)

    input_type = "keyboard"

    """
    Main Loop
    """

    while go:
        pygame.mouse.get_rel()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                return 0

            if input_type == "mouse":
                if event.type == pygame.MOUSEMOTION:
                    mx, my = pygame.mouse.get_pos()
                    x_max = worldx - player.image.get_size()[0]

                    if pygame.mouse.get_focused():
                        pygame.mouse.set_visible(False)
                        if mx < x_max:
                            dx, dy = pygame.mouse.get_rel()
                            player.control(dx/steps, 0)
                    else:
                        if pygame.mouse.get_visible() is False:
                            pygame.mouse.set_visible(True)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    player.jump()

            elif input_type == "keyboard":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        player.control(-steps, 0)
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        player.control(steps, 0)
                    if (event.key == pygame.K_UP or event.key == ord('w')
                            or event.key == pygame.K_SPACE):
                        player.jump()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        player.control(steps, 0)
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        player.control(-steps, 0)
            else:
                raise ValueError("Invalid input type: {}".format(input_type))

            if event.type == pygame.KEYDOWN:
                if event.key == ord('q'):
                    pygame.quit()
                    return 0
                if event.key == ord('i'):
                    if input_type == "keyboard":
                        input_type = "mouse"
                        if pygame.mouse.get_focused():
                            pygame.mouse.set_visible(False)
                    elif input_type == "mouse":
                        input_type = "keyboard"
                        pygame.mouse.set_visible(True)
                    else:
                        raise ValueError(
                            "Invalid input type: {}".format(input_type))
                    player.stop()

        if player.rect.x >= forwardx:
            scroll = player.rect.x - forwardx
            player.rect.x = forwardx
            for p in plat_list:
                p.rect.x -= scroll
            for e in enemy_list:
                e.rect.x -= scroll
            for l in loot_list:
                l.rect.x -= scroll

        if player.rect.x <= backwardx:
            scroll = backwardx - player.rect.x
            player.rect.x = backwardx
            for p in plat_list:
                p.rect.x += scroll
            for e in enemy_list:
                e.rect.x += scroll
            for l in loot_list:
                l.rect.x += scroll

        # TODO Implement vertical scroll -- take care of jump in

        world.blit(backdrop, backdropbox)
        player.update(enemy_list, ground_list, plat_list, loot_list, tx, ty)
        player.gravity(ty)

        ground_list.draw(world)
        plat_list.draw(world)
        player_list.draw(world)

        enemy_list.draw(world)
        for enemy in enemy_list:
            enemy.move()
            enemy.gravity(ty)
            enemy.update(player_list, ground_list, plat_list)

        loot_list.draw(world)

        pygame.display.flip()
        clock.tick(fps)

    return 0


if __name__ == '__main__':
    main()
