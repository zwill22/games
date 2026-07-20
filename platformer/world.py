import os
import pygame

import pygame.freetype

from platformer.objects import Player
from platformer.levels import level
from platformer.engine import SpriteList
from platformer.objects import Throwable


def stats(world, font: pygame.freetype.Font, score: int, health: int):
    """
    Display the current score and health of the player

    :param world: Game world in which to render stats
    :param font: Font for rendering stats
    :param score: Current score
    :param health: Current health
    """
    font.render_to(
        world, (4, 4), "Score: {}".format(score), (23, 23, 23), None, size=64
    )
    font.render_to(
        world, (4, 72), "Health: {}".format(health), (23, 23, 23), None, size=64
    )


def setup_firepower(player: Player):
    fire_images = ["fire-{}.png".format(i) for i in range(1)]
    fire = Throwable(player.rect.x, player.rect.y, *fire_images)
    # TODO Move out of file

    return fire, SpriteList()


class World:
    def __init__(self, world_x, world_y, tx, ty, edges):
        self.world_x = world_x
        self.world_y = world_y

        self.tx = tx
        self.ty = ty
        self.edges = edges

        self.world = pygame.display.set_mode([world_x, world_y])
        self.backdrop = pygame.image.load(os.path.join("images", "stage.png"))

        # Player setup
        self.player = Player(0, world_y / 2)

        # Firepower setup
        self.fire, self.firepower = setup_firepower(self.player)

        self.reinitialise_lists()

    def reinitialise_lists(self):
        self.ground_list = level.ground(1, self.tx, self.ty, self.world_y)
        self.plat_list = level.platform(1, self.tx, self.ty, self.world_y)
        self.enemy_list = level.enemies(1, self.tx, self.ty, self.world_y)
        self.loot_list = level.loot(1, self.tx, self.ty, self.world_y)

    def scroll_objects_x(self, fx, scroll):
        self.player.rect.x = fx

        for ob_list in (
            self.plat_list,
            self.enemy_list,
            self.loot_list,
            self.ground_list,
        ):
            for ob in ob_list:
                ob.rect.x += scroll

    def scroll_objects_y(self, fy, scroll):
        self.player.rect.y = fy

        for ob_list in (
            self.plat_list,
            self.enemy_list,
            self.loot_list,
            self.ground_list,
        ):
            for ob in ob_list:
                ob.rect.y += scroll

    def scroll(self):
        assert len(self.edges) == 4
        bx, fx, by, fy = self.edges

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
                self.player.rect.x,
                self.player.rect.y,
                "fire-0.png",
                throw=True,
                forward=self.player.facing_right,
            )
            pygame.mixer.Sound.play(flame)
            self.firepower.add(self.fire)

    def update(self):
        self.world.blit(self.backdrop, self.world.get_rect())

        self.player.update(
            self.enemy_list,
            self.ground_list,
            self.plat_list,
            self.loot_list,
            self.world_y,
        )

        self.player.gravity()

        for ob_list in (
            self.ground_list,
            self.plat_list,
            self.player,
            self.enemy_list,
            self.loot_list,
        ):
            ob_list.draw(self.world)

        if self.fire.firing:
            self.fire.update(self.world_x, self.world_y)
            self.firepower.draw(self.world)

        for enemy in self.enemy_list:
            enemy.move()
            enemy.gravity(self.world_y, self.ty)
            enemy.update(
                self.player,
                self.enemy_list,
                self.ground_list,
                self.plat_list,
                self.firepower,
            )

        for loot in self.loot_list:
            loot.update()
            
        if self.player.reset_required:
             self.player.reset()
             self.reinitialise_lists()

    def stats(self, font):
        stats(self.world, font, self.player.score, self.player.health)

