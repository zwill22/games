#!/usr/bin/env python3
# by Zack M. Williams
import os.path

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

import pygame.freetype

import level
from variables import worldx, worldy, fps
from objects import Player, Throwable
from code.engine import SpriteList

"""
TODO list
- animate fireballs
- animate loot
- health loot
- throwable items disintegrate on collision with platforms
- animate destruction of objects
- level goal
- more platforms
- More enemies
- PS4 controller
- App?
- Menus
- Settings file
- Move global variables to settings file
- Vertical movement
- Edge of maps
- Levels
- More consistent theme

- Cutscenes?
- Plot?

- Reorganise files

- death by jumping?
- Double jump?
- Bouncy objects?

- Hills?
- More scenery (scrolling)
"""


def stats(world, font: pygame.freetype.Font, score: int, health: int):
    """
    Display the current score and health of the player

    :param world: Game world in which to render stats
    :param font: Font for rendering stats
    :param score: Current score
    :param health: Current health
    """
    font.render_to(world, (4, 4), "Score: {}".format(score),
                   (23, 23, 23),None, size=64)
    font.render_to(world, (4, 72), "Health: {}".format(health),
                   (23, 23, 23), None, size=64)


def setup_firepower(player: Player):
    fire_images = ['fire-{}.png'.format(i) for i in range(1)]
    fire = Throwable(player.rect.x, player.rect.y, *fire_images)
    # TODO Move out of file

    return fire, SpriteList()


class World:
    def __init__(self, tx, ty):
        self.world = pygame.display.set_mode([worldx, worldy])
        self.backdrop = pygame.image.load(os.path.join('images', 'stage.png'))

        # Player setup
        self.player = Player(0, worldy/2)

        # Firepower setup
        self.fire, self.firepower = setup_firepower(self.player)

        # Platform/Ground setup
        gloc = []

        i = 0
        while i < (worldx / tx) + tx:
            gloc.append(i * tx)
            i += 1

        self.ground_list = level.ground(1, gloc, tx, ty)
        self.plat_list = level.platform(1, tx, ty)

        # Enemy and loot setup
        enemy_loc = [self.plat_list.sprites()[1].rect.x,
                self.plat_list.sprites()[1].rect.y - ty]
        self.enemy_list = level.bad(1, enemy_loc)

        self.loot_list = level.loot(1, tx, ty)

    def scroll_objects_x(self, fx, scroll):
        self.player.rect.x = fx

        for ob_list in (self.plat_list, self.enemy_list, self.loot_list):
            for ob in ob_list:
                ob.rect.x += scroll

    def scroll_objects_y(self, fy, scroll):
        self.player.rect.y = fy

        for ob_list in (self.plat_list, self.enemy_list, self.loot_list,
                        self.ground_list):
            for ob in ob_list:
                ob.rect.y += scroll

    def scroll(self, bx, fx, by, fy):
        if self.player.rect.x >= fx:
            scroll = self.player.rect.x - fx
            self.scroll_objects_x(fx, -scroll)

        if self.player.rect.x <= bx:
            scroll = bx - self.player.rect.x
            self.scroll_objects_x(bx, scroll)

        if self.player.rect.y >= fy:
            scroll = self.player.rect.y - fy
            self.scroll_objects_y(fy, -scroll)

        if self.player.rect.y <= by:
            scroll = by - self.player.rect.y
            self.scroll_objects_y(by, scroll)

    def fireball(self, flame):
        if not self.fire.firing:
            self.fire = Throwable(
                self.player.rect.x, self.player.rect.y, 'fire-0.png',
                throw=True, forward=self.player.facing_right)
            pygame.mixer.Sound.play(flame)
            self.firepower.add(self.fire)

    def update(self, tx, ty):
        self.world.blit(self.backdrop, self.world.get_rect())

        self.player.update(self.enemy_list, self.ground_list, self.plat_list,
                           self.loot_list, tx, ty)
        self.player.gravity()

        for ob_list in (self.ground_list, self.plat_list, self.player,
                        self.enemy_list, self.loot_list):
            ob_list.draw(self.world)

        if self.fire.firing:
            self.fire.update()
            self.firepower.draw(self.world)

        for enemy in self.enemy_list:
            enemy.move()
            enemy.gravity(ty)
            enemy.update(self.player, self.enemy_list, self.ground_list,
                         self.plat_list, self.firepower)

    def stats(self, font):
        stats(self.world, font, self.player.score, self.player.health)


def main():

    tx = 64
    ty = 64
    steps = 10
    input_type = "keyboard"

    edges = (0.3 * worldx, 0.7 * worldx, 0.17 * worldy, 0.83 * worldy)

    """
    Setup
    """
    clock = pygame.time.Clock()
    pygame.init()

    world = World(tx, ty)

    player = world.player

    # Font setup
    font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             "fonts", "Clickuper.ttf")
    fontsize = tx
    pygame.freetype.init()
    my_font = pygame.freetype.Font(font_path, size=fontsize)

    # Sounds
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join('sound', 'ObservingTheStar.ogg'))
    pygame.mixer.music.play(-1)

    flame = pygame.mixer.Sound(os.path.join('sound', 'flame.ogg'))

    """
    Main Loop
    """

    while True:
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
                        player.facing_right = False
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        player.control(steps, 0)
                        player.facing_right = True
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        player.jump()
                    if event.key == pygame.K_SPACE:
                        world.fireball(flame)

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

        world.scroll(*edges)

        world.update(tx, ty)
        world.stats(my_font)

        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main()
