# Нашествие монстров

Второй проект для Я.Лицея. На базе pygame.

# Структура проекта

- `bullet.py` - класс для вывода и перемешения пули
- `db.py` - функции для работы с БД (сохранение и получение данных)
- `db.sqlite` - БД sqlite
- `game.py` - класс игры (геймплей, управление героями и т.д.)
- `main.py` - запуск игры
- `monster.py` - класс для вывода и перемещения монстров
- `player.py` - класс для вывода и перемещения героя и его оружия
- `requirements.txt` - зависимости от других python библиотек
- `settings.py` - настройки игры
- `ui.py` - класс для управления кнопками
- `data` - директория, где хранятся картинки монстров, игрока и шрифт


# Правила игры



# Используемые ресурсы

Персонажи:
- https://rgsdev.itch.io/free-cc0-modular-animated-vector-characters-2d

Фон:
- https://craftpix.net/product/2d-horizontal-battle-backgrounds/

Шрифт:
- https://www.fonts.uprock.ru/fonts/porspican


# Литература

- Учим Python, делая крутые игры. Эл Свейгарт. 4-е изд. 2018.
- Изучаем Python: программирование игр, визуализация данных, веб-приложения. Мэтиз Эрик. 3-е изд. 2020.

# Что можно улучшить

- засекать время игры (и учитывать в рейтинге)
- выбирать персонаж главного героя
- сохранение в файл настроек игры
  - имя
  - персонаж
- устанавливать макс. кол-во патронов на уровень
- добавить новые виды оружия
- добавить новые виды монстров


# Про пересечения

- https://stackoverflow.com/questions/65361582/how-to-get-the-correct-dimensions-for-a-pygame-rectangle-created-from-an-image/65361896#65361896
- https://stackoverflow.com/questions/74973872/how-to-pin-an-image-in-the-center-of-sprite-rect/74973887#74973887
- https://github.com/Rabbid76/PyGameExamplesAndAnswers/blob/master/documentation/pygame/pygame_sprite_and_sprite_mask.md
- https://devdocs.io/pygame/ref/sprite