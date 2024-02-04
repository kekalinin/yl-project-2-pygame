import random
import sys
import pygame
import pygame_gui

import bullet
import monster
import player
import settings
import ui


class Game:
    """
    Класс для управления игрой.
    """

    # Событие и период в мс для создания нового монстра
    NEW_MONSTER_EVENT = pygame.USEREVENT + 1
    NEW_MONSTER_TIMEOUT = 1000

    # Координаты, где будем показывать диалоги
    DIALOG_X, DIALOG_Y = settings.SCREEN_WIDTH // 3, settings.SCREEN_HEIGHT // 3

    # Габариты по Y, где могут появляться герой или монстры
    MIN_Y, MAX_Y = 150, settings.SCREEN_HEIGHT - 300

    # Уровни игры
    LEVELS = {
        1: {
            'monsters': 10,     # Кол-во монстров на уровне
            'speed': 2,         # Скорость приближения монстра
            'lives': 3,         # Кол-во жизней у героя
            'points': 10,       # Кол-во очков за убийство монстра
        },
        2: {
            'monsters': 20,
            'speed': 4,
            'lives': 2,
            'points': 20,
        },
        3: {
            'monsters': 30,
            'speed': 6,
            'lives': 1,
            'points': 30,
        }
    }

    def __init__(self):
        """
        Инициализирует игру и создает игровые ресурсы.
        """

        self.score = 0
        self.user_name = "Игрок 1"

        # играем или нет?
        self.game_running = False
        self.game_level = 1
        self.lives = 0
        self.monsters_max = 0
        self.monsters_created = 0

        self.player = player.Player(self.MIN_Y, self.MAX_Y)
        self.bullets = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()

        pygame.init()

        self.screen = pygame.display.set_mode(settings.SCREEN_SIZE)
        pygame.display.set_caption(settings.TITLE)

        self.bg_image_src = pygame.image.load('data/bg.jpeg')
        self.bg_image = pygame.transform.scale(self.bg_image_src, settings.SCREEN_SIZE)

        self.ui_manager = pygame_gui.UIManager(settings.SCREEN_SIZE)

        # граница по X, по которой будут все кнопки выровнены
        button_x = settings.SCREEN_WIDTH // 2 - settings.BUTTON_WIDTH // 2
        self.controls = ui.Controls(button_x, self.user_name, self.ui_manager)

        pygame.time.set_timer(self.NEW_MONSTER_EVENT, self.NEW_MONSTER_TIMEOUT)

        # Ожидаем ли подтверждение выхода из игры
        self.wait_confirm_exit = False
        # Ожидаем ли подтверждение начала игры
        self.wait_start_game = False

    def _show_bg(self):
        """
        Показывает фон
        """
        self.screen.blit(self.bg_image, (0, 0))

        font = pygame.font.Font('./data/PorspicanSerif-Regular.otf', 60)
        text = font.render(settings.TITLE, True, pygame.Color('white'))
        text_x = settings.SCREEN_WIDTH // 2 - text.get_width() // 2
        text_y = 50
        self.screen.blit(text, (text_x, text_y))

    def _show_score(self):
        """
        Выводит счет игрока во время игры.
        """
        # font = pygame.font.Font(None, 20)
        font = pygame.font.Font('./data/PorspicanSerif-Regular.otf', 14)
        info = f"Игрок: {self.user_name}\n" \
               f"Очки: {self.score}\n" \
               f"Жизней: {self.lives}\n" \
               f"Монстров: живых={len(self.monsters)}, создано={self.monsters_created}, всего={self.monsters_max}\n" \
               f"Уровень: {self.game_level}"
        text = font.render(info, True, pygame.Color('gray'))
        text_x = 20
        text_y = 20
        self.screen.blit(text, (text_x, text_y))

    def show_start_view(self):
        """
        Запуск экрана заставки
        """
        self._show_bg()

    def _check_monsters_hit(self):
        """
        Проверяет попадание пуль в монстров.
        """
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.monsters, True, True)
        if collisions:
            self.score += self.LEVELS[self.game_level]['points']

    def _check_player_hit(self):
        """
        Проверяет, дотронулся ли монстр до игрока.
        """
        collision = pygame.sprite.spritecollideany(self.player, self.monsters)
        if collision:
            collision.kill()
            self.lives -= 1

            if self.lives < 0:
                self.game_running = False
                self.wait_confirm_exit = True
                pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((self.DIALOG_X, self.DIALOG_Y), (300, 200)),
                    manager=self.ui_manager,
                    window_title="Вы проиграли :(",
                    action_long_desc=f"Игра окончена.\nЗаработано очков: {self.score}",
                    blocking=True
                )

                # возвращаемся на первый уровень
                self.game_level = 1
                self._set_level_conditions()

    def _check_level_end(self):
        """
        Проверяет, закончился ли уровень
        (на экране никого нет и не надо больше новых создавать).
        """

        if self.monsters_created >= self.monsters_max and len(self.monsters) == 0:
            old_level = self.game_level
            self.game_level += 1

            # если прошли все уровни
            if self.game_level > max(self.LEVELS.keys()):
                self.game_running = False
                pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((self.DIALOG_X, self.DIALOG_Y), (400, 250)),
                    manager=self.ui_manager,
                    window_title=f"Вы прошли игру!",
                    action_long_desc=f"Вы прошли игру! Респект!\n"
                                     f"Кол-во очков: {self.score}.",
                    blocking=True
                )
                # возвращаемся на первый уровень
                self.game_level = 1
                self._set_level_conditions()
                return

            self._set_level_conditions()
            cnt = self.LEVELS[self.game_level]['monsters']
            speed = self.LEVELS[self.game_level]['speed']
            pygame_gui.windows.UIConfirmationDialog(
                rect=pygame.Rect((self.DIALOG_X, self.DIALOG_Y), (400, 250)),
                manager=self.ui_manager,
                window_title=f"Вы закончили уровень #{old_level}!",
                action_long_desc=f"Теперь необходимо уничтожить {cnt} монстров.\n"
                                 f"Они двигаются со скоростью: {speed}.\n"
                                 "Go-go-go!",
                blocking=True
            )

    def render(self):
        self._show_bg()

        if not self.game_running:
            self.controls.show()
            return

        self.controls.hide()

        self.player.render(self.screen)

        self.bullets.draw(self.screen)
        self.bullets.update()

        self.monsters.draw(self.screen)
        self.monsters.update()

        self._check_monsters_hit()
        self._check_player_hit()
        self._check_level_end()

        self._show_score()

    def run(self):
        """
        Запуск основного цикла игры.
        """

        self.show_start_view()

        clock = pygame.time.Clock()
        while True:
            time_delta = clock.tick(60) / 1000.0
            self._check_events()
            self.render()
            self.ui_manager.update(time_delta)
            self.ui_manager.draw_ui(self.screen)

            # Отображение последнего прорисованного экрана.
            pygame.display.flip()

    def _set_level_conditions(self):
        """
        Выставляет условия текущего уровня.
        """
        self.lives = self.LEVELS[self.game_level]['lives']
        self.monsters_max = self.LEVELS[self.game_level]['monsters']
        self.monsters_created = 0

    def _create_monster(self):
        """
        Создает нового монстра в случайной позиции.
        Тип монстра зависит от текущего уровня игры.
        """
        m = monster.Monster(self.monsters, type_id=self.game_level)
        m.speed = self.LEVELS[self.game_level]['speed']
        m.rect.x = settings.SCREEN_WIDTH - 150
        m.rect.y = random.randint(self.MIN_Y, self.MAX_Y)
        self.monsters_created += 1

    def _check_events(self):
        """
        Обрабатывает нажатия клавиш и событий.
        """
        for event in pygame.event.get():
            # pygame
            if event.type == pygame.QUIT:
                sys.exit()
            if self.game_running:
                if event.type == self.NEW_MONSTER_EVENT:
                    # Кол-во монстров не должно быть более, чем макс. для уровня
                    if self.monsters_created >= self.monsters_max:
                        continue
                    self._create_monster()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.shoot()
                        pos = self.player.get_shoot_rect()
                        b = bullet.Bullet(self.bullets)
                        b.rect.x = pos.x
                        b.rect.y = pos.y

                    if event.key == pygame.K_ESCAPE:
                        self.wait_confirm_exit = True
                        pygame_gui.windows.UIConfirmationDialog(
                            rect=pygame.Rect((self.DIALOG_X, self.DIALOG_Y), (300, 200)),
                            manager=self.ui_manager,
                            window_title="Заканчиваем?",
                            action_long_desc="Хотите закончить игру?",
                            blocking=True
                        )
                if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
                    self.player.move_down()
                if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
                    self.player.move_up()

            # gui
            if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                if self.wait_confirm_exit:
                    self.game_running = False
                    self.wait_confirm_exit = False

                if self.wait_start_game:
                    self.game_running = True
                    self.wait_start_game = False
                    self._set_level_conditions()

            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                self.user_name = event.text

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                # если нажали на кнопку мыши не на элементе - игнорируем
                if not event.dict.get('ui_element'):
                    continue
                if event.ui_element == self.controls.button_exit:
                    sys.exit()
                if event.ui_element == self.controls.button_start:
                    # Сохраняем последнее указанное имя
                    self.user_name = self.controls.button_user_name.text

                    cnt = self.LEVELS[self.game_level]['monsters']
                    speed = self.LEVELS[self.game_level]['speed']
                    self.wait_start_game = True
                    pygame_gui.windows.UIConfirmationDialog(
                        rect=pygame.Rect((self.DIALOG_X, self.DIALOG_Y), (400, 240)),
                        manager=self.ui_manager,
                        window_title=f"Начинаем играть! Уровень: {self.game_level}",
                        action_long_desc=f"Необходимо уничтожить {cnt} монстров.\n"
                                         f"Они двигаются со скоростью: {speed}.\n"
                                         "Начинаем?",
                        blocking=True
                    )

            self.ui_manager.process_events(event)
