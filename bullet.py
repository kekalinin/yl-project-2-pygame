import pygame

import settings


class Bullet(pygame.sprite.Sprite):
    """
    Класс для управления снарядами.
    """

    scale = 0.02
    speed = 10

    def __init__(self, *group):
        """
        Создает объект снарядов в текущей позиции корабля.
        """
        super(Bullet, self).__init__(*group)

        self.image_src = pygame.image.load(f'data/bullet.png')
        self.image = pygame.transform.scale_by(self.image_src, self.scale)
        self.rect = self.image.get_bounding_rect()
        if settings.SHOW_BORDERS:
            pygame.draw.rect(self.image, pygame.Color('yellow'), self.rect, 1)

    def update(self):
        """
        Перемещает снаряд по экрану.
        """
        self.rect.x += self.speed
        # удаляем, если ушли за границы экрана
        if self.rect.x >= settings.SCREEN_WIDTH:
            self.kill()
