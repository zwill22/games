from ..engine import Sprite


class Player(Sprite):
    """
    Spawn a player
    """

    def __init__(self, x, y, **kwargs):
        hero = ["hero-{}.png".format(i) for i in range(4)]

        Sprite.__init__(self, x, y, *hero, **kwargs)
        self.frame = 0
        self.health = 10
        self.damage = False
        self.score = 0

        self.is_jumping = True
        self.is_falling = False

        self.facing_right = True

    def gravity(self):
        if self.is_jumping:
            self.move_y += 2

    def jump(self):
        if not self.is_jumping:
            self.is_falling = False
            self.is_jumping = True

    def update(self, enemy_list, ground_list, plat_list, loot_list, world_x,
               world_y, tx, ty):
        """
        Update sprite position
        """
        self.update_sprite()

        if self.move_x < 0 or self.move_x > 0:
            self.is_jumping = True

        enemy_hit_list = self.hit_list(enemy_list)
        if not self.damage:
            for enemy in enemy_list:
                if not self.rect.contains(enemy):
                    self.damage = self.rect.colliderect(enemy)
        if self.damage:
            idx = self.rect.collidelist(enemy_hit_list)
            if idx == -1:
                self.damage = 0
                self.health -= 1

        ground_hit_list = self.hit_list(ground_list)
        for g in ground_hit_list:
            self.move_y = 0
            self.rect.bottom = g.rect.top
            self.is_jumping = False

        loot_hit_list = self.hit_list(loot_list)
        for loot in loot_hit_list:
            loot_list.remove(loot)
            self.score += 1

        plat_hit_list = self.hit_list(plat_list)
        for p in plat_hit_list:
            self.is_jumping = False
            self.move_y = 0

            # approach from below
            if self.rect.bottom < p.rect.bottom:
                self.rect.bottom = p.rect.top
            else:
                self.move_y += 2

        # Fall off the world
        if self.rect.y > world_y:
            self.health -= 1
            self.rect.x = tx
            self.rect.y = ty

        if self.is_jumping and not self.is_falling:
            self.is_falling = True
            self.move_y -= 24
