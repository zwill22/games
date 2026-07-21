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

from pathlib import Path

import pygame
import pygame.freetype

from platformer.world import World

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


def main():
    tx = 64
    ty = 64
    
    world_x = 16 * tx
    world_y = 12 * ty
    fps = 40
    steps = 10
    input_type = "keyboard"

    edges = (0.3 * world_x, 0.7 * world_x, 0.17 * world_y, 0.83 * world_y)

    """
    Setup
    """
    clock = pygame.time.Clock()
    pygame.init()

    font = Path("fonts")
    audio = Path("audio")

    # Fonts
    pygame.freetype.init()
    fonts = {"main": pygame.freetype.Font(font / "Clickuper.ttf", size=tx)}

    # Sounds
    mute = False
    pygame.mixer.init()
    pygame.mixer.music.load(audio / "ObservingTheStar.ogg")
    pygame.mixer.music.play(-1)

    sounds = {
        "flame": pygame.mixer.Sound(audio / "flame.ogg"),
        "burn": pygame.mixer.Sound(audio / "fire_sound_effect.mp3"),
    }

    world = World(world_x, world_y, tx, ty, edges, sounds)

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
                    mx, _ = pygame.mouse.get_pos()
                    x_max = world.get_x_max()

                    if pygame.mouse.get_focused():
                        pygame.mouse.set_visible(False)
                        if mx < x_max:
                            dx, _ = pygame.mouse.get_rel()
                            world.control_player(dx / steps, 0)
                    else:
                        if pygame.mouse.get_visible() is False:
                            pygame.mouse.set_visible(True)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    world.make_player_jump()

            elif input_type == "keyboard":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == ord("a"):
                        world.control_player(-steps, 0)
                        world.player_left()
                    if event.key == pygame.K_RIGHT or event.key == ord("d"):
                        world.control_player(steps, 0)
                        world.player_right()
                    if event.key == pygame.K_UP or event.key == ord("w"):
                        world.make_player_jump()
                    if event.key == pygame.K_SPACE:
                        world.fireball(sounds)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == ord("a"):
                        world.control_player(steps, 0)
                    if event.key == pygame.K_RIGHT or event.key == ord("d"):
                        world.control_player(-steps, 0)
            else:
                raise ValueError("Invalid input type: {}".format(input_type))

            if event.type == pygame.KEYDOWN:
                if event.key == ord("q") or event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return 0
                if event.key == ord("i"):
                    if input_type == "keyboard":
                        input_type = "mouse"
                        if pygame.mouse.get_focused():
                            pygame.mouse.set_visible(False)
                    elif input_type == "mouse":
                        input_type = "keyboard"
                        pygame.mouse.set_visible(True)
                    else:
                        raise ValueError("Invalid input type: {}".format(input_type))
                    world.stop_player()
                if event.key == ord("m"):
                    volume = 1 if mute else 0

                    pygame.mixer.music.set_volume(volume)
                    for sound in sounds.values():
                        sound.set_volume(volume)
                    mute = not mute

        if world.game_over():
            world.game_over_screen(fonts["main"], mute)
        else:
            world.scroll()
            world.update()
            world.show_stats(fonts["main"], mute)

        pygame.display.flip()
        clock.tick(fps)


if __name__ == "__main__":
    main()
