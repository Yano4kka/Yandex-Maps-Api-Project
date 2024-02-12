import pygame
import os

pygame.init()


def print_on_screen(screen, text):
    font = pygame.font.Font(None, text[3])
    string_rendered = font.render(text[0], 1, pygame.Color((120, 31, 25)))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = text[2]
    intro_rect.x = text[1]
    screen.blit(string_rendered, intro_rect)


def load_image(name, colorkey=None):  # функция для загрузки картинки (взята из учебника)
    fullname = os.path.join('data', name)
    if name == 'сброс.jpg':
        image = pygame.image.load(fullname)
        image = pygame.transform.scale(image, (30, 30))
    elif name == 'mail_index_off.png' or name == 'mail_index_on.png':
        image = pygame.image.load(fullname)
        image = pygame.transform.scale(image, (30, 30))
    else:
        image = pygame.image.load(fullname)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Options(pygame.sprite.Sprite):
    def __init__(self, im, x, y, options_group):
        super().__init__(options_group)
        self.image = load_image(im, 1)
        self.rect = self.image.get_rect().move(x, y)
        self.im = im


class Options2(pygame.sprite.Sprite):
    def __init__(self, im, x, y, options_group):
        super().__init__(options_group)
        self.image = load_image(im, 1)
        self.rect = self.image.get_rect().move(x, y)
        self.im = im