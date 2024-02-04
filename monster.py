import pygame

import settings

# Чтобы не загружать каждый раз картинку, делаем это один раз
# И складываем (кэшируем) в эту переменную.
IMAGES = {}


class Monster(pygame.sprite.Sprite):
    """
    Класс для управления монстром.

    Наследуется от спрайта, т.к. их может быть много на экране,
    спрайты работают быстрее (выводятся группой сразу).
    """

    speed = 1
    scale = 0.1

    def __init__(self, *group, type_id: int = 1):
        """
        Создает монстра.
        """
        super(Monster, self).__init__(*group)

        self.count_images = 8
        self.curr_image = 0

        self.images = IMAGES.get(type_id, [])
        self.image = None

        if not self.images:
            for n in range(self.count_images):
                tmp = pygame.image.load(f'data/monster/{type_id}/walk_{n}.png')
                tmp = tmp.subsurface(tmp.get_bounding_rect())
                self.images.append(
                    pygame.transform.scale_by(pygame.transform.flip(tmp, flip_x=True, flip_y=False),
                                              self.scale))
                if settings.SHOW_BORDERS:
                    pygame.draw.rect(self.images[-1], pygame.Color('blue'),
                                     self.images[-1].get_rect(), 1)
            IMAGES[type_id] = self.images
        self.rect = self.images[-1].get_rect()

        self._choose_image()

    def _choose_image(self):
        """
        Выбирает картинку из списка (анимация)
        """
        self.curr_image = (self.curr_image + 1) % self.count_images
        self.image = self.images[self.curr_image]

    def update(self):
        """
        Перемещает монстра по экрану.
        """
        self.rect.x -= self.speed
        # удаляем, если ушли за границы экрана
        if self.rect.x < 0:
            self.kill()
        if self.rect.x % 10 == 0:
            self._choose_image()

