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
import os

ani = 4


class Player(pygame.sprite.Sprite):
    """
    Spawn a player
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.health = 10

        self.images = []
        for i in range(4):
            img = pygame.image.load(
                os.path.join('images', 'hero-{}.png'.format(i))
            ).convert()
            img.convert_alpha()
            img.set_colorkey(0)
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

    def control(self, x, y):
        """
        Control player movement
        """
        self.movex += x
        self.movey += y

    def stop(self):
        """
        Stop player movement
        """
        self.movex = 0
        self.movey = 0

    def update(self, enemy_list):
        """
        Update sprite position
        """
        self.rect.x += self.movex
        self.rect.y += self.movey

        if self.movex < 0 or self.movex > 0:
            self.frame += 1
            if self.frame > 3 * ani:
                self.frame = 0

        if self.movex < 0:
            self.image = pygame.transform.flip(
                self.images[self.frame//ani], True, False
            )

        if self.movex > 0:
            self.image = self.images[self.frame//ani]

        hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        for enemy in hit_list:
            self.health -= 1
        print("Player health: {}".format(self.health))


class Enemy(pygame.sprite.Sprite):
    """
    Spawn an enemy
    """
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)

        self.images = []
        for i in range(4):
            im = pygame.image.load(
                os.path.join('images', '{}-{}.png'.format(img, i))
            ).convert()
            im.convert_alpha()
            im.set_colorkey(0)
            self.images.append(im)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.counter = 0

    def move(self):
        """
        Enemy movement
        """
        distance = 50
        speed = 6

        if 0 <= self.counter < distance:
            self.rect.x += speed
        elif distance <= self.counter <= distance * 2:
            self.rect.x -= speed
        else:
            self.counter = 0

        self.counter += 1


class Level:
    def bad(self, lvl, eloc):
        if lvl == 1:
            enemy = Enemy(eloc[0], eloc[1], 'enemy')
            enemy_list = pygame.sprite.Group()
            enemy_list.add(enemy)
        else:
            ValueError("Invalid level: {}".format(lvl))

        return enemy_list


def main():
    """
    Variables
    """
    worldx = 960
    worldy = 720
    fps = 40
    go = True

    """
    Objects
    """

    """
    Setup
    """
    clock = pygame.time.Clock()
    pygame.init()

    world = pygame.display.set_mode([worldx, worldy])
    backdrop = pygame.image.load('images/stage.png')
    backdropbox = world.get_rect()

    player = Player()
    player.rect.x = 0
    player.rect.y = 0
    player_list = pygame.sprite.Group()
    player_list.add(player)
    steps = 10

    enemy_list = Level.bad(1, [300, 0])

    input_type = "keyboard"

    """
    Main Loop
    """

    while go:
        pygame.mouse.get_rel()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                try:
                    sys.exit()
                finally:
                    go = False

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
                    # TODO Program for one button only
                    print("jump")

            elif input_type == "keyboard":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        player.control(-steps, 0)
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        player.control(steps, 0)
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        print('jump')

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
                    try:
                        sys.exit()
                    finally:
                        go = False
                if event.key == ord('i'):
                    if input_type == "keyboard":
                        input_type = "mouse"
                        if pygame.mouse.get_focused():
                            pygame.mouse.set_visible(False)
                    elif input_type == "mouse":
                        input_type = "keyboard"
                        pygame.mouse.set_visible(True)
                    else:
                        raise ValueError("Invalid input type: {}".format(input_type))
                    player.stop()

        world.blit(backdrop, backdropbox)
        player.update(enemy_list)
        player_list.draw(world)
        enemy_list.draw(world)
        for e in enemy_list:
            e.move()
        pygame.display.flip()
        clock.tick(fps)

    return 0


if __name__ == '__main__':
    main()
