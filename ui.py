import pygame
import pygame_gui

import settings


class Controls:
    """
    Управление кнопками игры
    """

    def __init__(self, x, user_name, ui_manager):
        self.button_user_name_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((x - 30, 300), (settings.BUTTON_WIDTH, settings.BUTTON_HEIGHT // 2)),
            text="Имя пользователя:",
            manager=ui_manager
        )

        self.button_user_name = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((x, 330), (settings.BUTTON_WIDTH, settings.BUTTON_HEIGHT // 2)),
            initial_text=user_name,
            manager=ui_manager
        )

        self.button_start = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((x, 400), settings.BUTTON_SIZE),
            text='Начать',
            manager=ui_manager
        )

        self.button_show_records = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((x, 500), settings.BUTTON_SIZE),
            text='Рекорды',
            manager=ui_manager
        )

        self.button_exit = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((x, 600), settings.BUTTON_SIZE),
            text='Выход',
            manager=ui_manager
        )

        # список всех элементов управления (чтобы потом массово показывать или прятать)
        self.controls = [
            self.button_user_name,
            self.button_user_name_label,
            self.button_start,
            self.button_show_records,
            self.button_exit,
        ]

    def hide(self):
        """
        Скрывает кнопки главного меню.
        """
        for c in self.controls:
            c.hide()

    def show(self):
        """
        Показывает кнопки главного меню.
        """
        for c in self.controls:
            c.show()

