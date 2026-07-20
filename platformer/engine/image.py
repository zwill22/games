import pygame

from pathlib import Path

image_path = Path("images")


def load_image(name: str):
    return pygame.image.load(image_path / name)
