import pygame.freetype

from platformer.objects import Player
from platformer.levels import level
from platformer.engine import SpriteList, load_image
from platformer.objects import Throwable


def game_over(world, font: pygame.freetype.Font, muted: bool):
    """
    Display the Game Over message on screen

    :param world: Game world in which to render stats
    :param font: Font for rendering text
    :param muted: Whether the sound is muted
    """
    w = world.get_width()
    h = world.get_height()
    s = 128

    x0 = w / 2 - s * 2
    y0 = h / 2 - s

    colour = (40, 40, 40)
    font.render_to(world, (x0, y0), "Game", colour, None, size=128)
    font.render_to(world, (x0, y0 + s), "Over!", colour, None, size=s)

    font.render_to(world, (x0, y0 + 2 * s), "Press 'q' to Quit", colour, None, size=32)

    if muted:
        font.render_to(world, (4, 8), "Muted", colour, None, size=64)


def setup_firepower(player: Player):

    fire_images = ["fire-{}.png".format(i) for i in range(1)]
    fire = Throwable(player.rect.x, player.rect.y, *fire_images)
    # TODO Move out of file

    return fire, SpriteList()


class World:
    def __init__(self, world_x, world_y, tx, ty, edges):
        self.tx = tx
        self.ty = ty
        self.edges = edges
        self.level = 1

        self.display = pygame.display.set_mode([world_x, world_y])

        self.setup_background(world_x, world_y)

        # Player setup
        self.player = Player(0, world_y / 2)

        # Firepower setup
        self.fire, self.firepower = setup_firepower(self.player)

        self.complete = False

        self.reinitialise_lists()

    def setup_background(self, world_x, world_y):
        self.backdrop = load_image(f"background-{self.level}.png")

        w = self.backdrop.get_width()
        h = self.backdrop.get_height()

        scale = max(world_x / w, world_y / h)

        w_new = scale * w
        h_new = scale * h

        self.offset = (w_new - world_x, h_new - world_y)

        self.backdrop = pygame.transform.scale(self.backdrop, (w_new, h_new))

    def reinitialise_lists(self):
        y = self.display.get_height()

        try:
            self.ground_list = level.ground(self.level, self.tx, self.ty, y)
            self.underground_list = level.underground(self.level, self.tx, self.ty, y)
            self.plat_list = level.platform(self.level, self.tx, self.ty, y)
            self.enemy_list = level.enemies(self.level, self.tx, self.ty, y)
            self.loot_list = level.loot(self.level, self.tx, self.ty, y)
        except ValueError:
            self.complete = True

    def get_x_max(self):
        return self.display.get_width() - self.player.image.get_width()

    def control_player(self, x, y):

        self.player.control(x, y)

    def player_left(self):
        self.player.facing_right = False

    def player_right(self):
        self.player.facing_right = True

    def game_over(self):
        return self.player.health <= 0 or self.complete

    def make_player_jump(self):
        self.player.jump()

    def stop_player(self):
        self.player.stop()

    def reset(self):
        self.player.reset()
        self.reinitialise_lists()

    def scroll_objects_x(self, fx, scroll):
        self.player.rect.x = fx

        for ob_list in (
            self.plat_list,
            self.enemy_list,
            self.loot_list,
            self.ground_list,
            self.underground_list,
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
            self.underground_list,
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

    def fireball(self, sounds):
        if not self.fire.firing:
            self.fire = Throwable(
                self.player.rect.x,
                self.player.rect.y,
                "fire-0.png",
                throw=True,
                forward=self.player.facing_right,
            )

            flame = sounds["flame"]
            pygame.mixer.Sound.play(flame)
            self.firepower.add(self.fire)

    def set_display(self):
        rect = self.display.get_rect()
        rect.x -= self.offset[0] / 2
        rect.y -= self.offset[1] / 2
        self.display.blit(self.backdrop, rect)

    def new_level(self):
        self.level += 1
        self.reset()

    def update(self):
        self.set_display()

        x = self.display.get_width()
        y = self.display.get_height()

        self.player.update(
            self.enemy_list,
            self.ground_list,
            self.plat_list,
            self.loot_list,
            y,
        )

        if self.player.level_complete:
            self.new_level()
            return

        if self.player.reset_required:
            self.reset()
            return

        self.player.gravity()

        for ob_list in (
            self.ground_list,
            self.underground_list,
            self.plat_list,
            self.player,
            self.enemy_list,
            self.loot_list,
        ):
            ob_list.draw(self.display)

        if self.fire.firing:
            self.fire.update(x, y)
            self.firepower.draw(self.display)

        for enemy in self.enemy_list:
            enemy.move()
            enemy.gravity(y, self.ty)
            enemy.update(
                self.player,
                self.enemy_list,
                self.ground_list,
                self.plat_list,
                self.firepower,
            )

        for loot in self.loot_list:
            loot.update()

    def show_stats(self, font, muted: bool):
        size = 64
        colour = (20, 20, 20)

        x0 = 4
        y0 = 8

        x = self.display.get_width()

        font.render_to(
            self.display,
            (x0, y0),
            f"Score: {self.player.score}",
            colour,
            None,
            size=size,
        )

        font.render_to(
            self.display,
            (x0, y0 + 64),
            f"Health: {self.player.health}",
            colour,
            None,
            size=size,
        )

        level = f"Level {self.level}"

        font.render_to(
            self.display, (x - 0.6 * size * len(level), y0), level, None, size=size
        )

        if muted:
            font.render_to(
                self.display,
                (x - 4 * size, y0 + size),
                "Muted",
                colour,
                None,
                size=size,
            )

    def game_over_screen(self, font, muted):
        self.set_display()

        game_over(self.display, font, muted)
