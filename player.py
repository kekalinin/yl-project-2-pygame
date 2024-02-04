import pygame

import settings


class Player:
    """
    Класс для управления игроком.
    """

    speed = 1
    scale = 0.1
    image = None
    curr_image = 0

    def __init__(self, min_y, max_y):
        self.images = []
        self.count_images = 8
        self.curr_weapon = 1

        for n in range(self.count_images):
            tmp = pygame.image.load(f'data/player/1/walk_{n}.png')
            tmp = tmp.subsurface(tmp.get_bounding_rect())
            self.images.append(pygame.transform.scale_by(tmp, self.scale))

        self.weapon_src = pygame.image.load(f'data/weapons/weaponR{self.curr_weapon}.png')
        self.weapon = pygame.transform.scale_by(self.weapon_src, 0.04)

        # Изображения выстрела
        self.muzzle_src = pygame.image.load(f'data/muzzle.png')
        self.muzzle = pygame.transform.scale_by(self.muzzle_src, 0.02)
        # Сколько кадров показывать (если > 0)
        self.shoot_timer = 0

        self.rect = self.images[self.curr_image].get_rect()
        self.rect.x = 20
        self.rect.y = settings.SCREEN_HEIGHT // 2
        self.min_y = min_y
        self.max_y = max_y

        self._choose_image()

    def _choose_image(self):
        self.curr_image = self.rect.y % self.count_images
        self.image = self.images[self.curr_image]

    def move_up(self):
        """
        Передвижение вверх.
        """
        self.rect.y = max(self.min_y, self.rect.y - self.speed)

    def move_down(self):
        """
        Передвижение вниз.
        """
        self.rect.y = min(self.max_y, self.rect.y + self.speed)

    def shoot(self):
        """
        Начало выстрела.
        """
        self.shoot_timer = 5

    def _render_weapon(self, screen: pygame.Surface):
        """
        Отрисовка оружия.
        """
        weapon_rect = self.rect.copy()
        screen.blit(self.weapon, weapon_rect)

    def _render_self(self, screen: pygame.Surface):
        """
        Отрисовка персонажа.
        """
        self._choose_image()
        screen.blit(self.image, self.rect)
        if settings.SHOW_BORDERS:
            pygame.draw.rect(screen, pygame.Color('red'), self.rect, 1)

    def get_shoot_rect(self):
        muzzle_rect = self.rect.copy()
        muzzle_rect.x += 55
        muzzle_rect.y += 35
        return muzzle_rect

    def _render_shoot(self, screen: pygame.Surface):
        """
        Отрисовка выстрела.
        """
        if self.shoot_timer:
            muzzle_rect = self.get_shoot_rect()
            screen.blit(self.muzzle, muzzle_rect)
            self.shoot_timer -= 1

    def render(self, screen: pygame.Surface):
        """
        Отрисовка игрока на экране
        """
        self._render_self(screen)
        self._render_weapon(screen)
        self._render_shoot(screen)

