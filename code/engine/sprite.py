import pygame

import os

# TODO Fix magic numbers
ani = 4


class Sprite(pygame.sprite.Sprite):
    """
    Generic sprite class based on pygame's Sprite class
    """
    def __init__(self, xloc, yloc, *images, image_dir='images', alpha=0):
        pygame.sprite.Sprite.__init__(self)

        self.images = []
        for image in images:
            img = pygame.image.load(os.path.join(image_dir, image)).convert()
            img.convert_alpha()
            img.set_colorkey(alpha)
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = xloc
        self.rect.y = yloc

        self.movex = 0
        self.movey = 0

        self.frame = 0

    def hit_list(self, ob_list):
        return pygame.sprite.spritecollide(self, ob_list, False)

    def hit(self, pysprite) -> bool:
        return pysprite.rect.colliderect(self.rect)

    def control(self, x, y):
        self.movex += x
        self.movey += y

    def stop(self):
        self.movex = 0
        self.movey = 0

    def draw(self, world):
        sprite_list = pygame.sprite.Group()
        sprite_list.add(self)
        sprite_list.draw(world)

    def update_sprite(self):
        n = len(self.images)

        if n > 1:
            if self.movex < 0 or self.movex > 0:
                self.frame += 1
                if self.frame > (n - 1) * ani:
                    self.frame = 0

        if self.movex < 0:
            self.image = pygame.transform.flip(
                self.images[self.frame//ani], True, False
            )

        if self.movex > 0:
            self.image = self.images[self.frame//ani]

        self.rect.x += self.movex
        self.rect.y += self.movey
