import pygame

import os


class SpriteList:
    """
    Wrapper for pygame's Group class
    """
    def __init__(self):
        self.list = pygame.sprite.Group()

    def add(self, sprite):
        self.list.add(sprite)

    def sprites(self):
        return self.list.sprites()

    def draw(self, world):
        self.list.draw(world)

    def remove(self, sprite):
        self.list.remove(sprite)

    def __iter__(self):
        return iter(self.list)


class Sprite(pygame.sprite.Sprite):
    """
    Generic sprite class based on pygame's Sprite class
    """
    def __init__(self, x_loc, y_loc, *images, image_dir='images', alpha=0,
                 ani=4):
        pygame.sprite.Sprite.__init__(self)

        self.images = []
        for image in images:
            img = pygame.image.load(os.path.join(image_dir, image)).convert()
            img.convert_alpha()
            img.set_colorkey(alpha)
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x_loc
        self.rect.y = y_loc

        self.move_x = 0
        self.move_y = 0

        self.frame = 0
        self.forward = True

        self.ani = ani

    def hit_list(self, ob_list):
        return pygame.sprite.spritecollide(self, ob_list, False)

    def hit(self, pysprite) -> bool:
        return pysprite.rect.colliderect(self.rect)

    def control(self, x, y):
        self.move_x += x
        self.move_y += y

    def stop(self):
        self.move_x = 0
        self.move_y = 0

    def draw(self, world):
        sprite_list = SpriteList()
        sprite_list.add(self)
        sprite_list.draw(world)

    def update_sprite(self):
        n = len(self.images)

        if n > 1:
            if self.move_x < 0 or self.move_x > 0:
                self.frame += 1
                if self.frame > (n - 1) * self.ani:
                    self.frame = 0

        if self.move_x < 0:
            self.image = pygame.transform.flip(
                self.images[self.frame//self.ani], True, False
            )

        if self.move_x > 0:
            self.image = self.images[self.frame//self.ani]

        self.rect.x += self.move_x
        self.rect.y += self.move_y
