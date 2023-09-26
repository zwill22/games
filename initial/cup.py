import pygame


class Cup(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('cup.svg').convert()

        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10


def main():
    pygame.init()

    screen = pygame.display.set_mode((960, 720))

    cup = Cup()

    while True:
        pygame.display.update()
        screen.blit(cup.image, cup.rect)


if __name__ == '__main__':
    main()
