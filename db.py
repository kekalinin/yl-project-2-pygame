import sqlite3
import time

import settings

GAME_TABLE = "game_stat"


def init_db():
    """
    Создает новую БД, если еще не создана.
    """
    con = sqlite3.connect(settings.DB_PATH)
    c = con.cursor()

    c.execute(f'''
    CREATE TABLE IF NOT EXISTS {GAME_TABLE} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name   TEXT     NOT NULL,
        dt          DATETIME NOT NULL,
        bullets     INTEGER  NOT NULL,
        points      INTEGER  NOT NULL
    )''')
    con.commit()


def add_new_record(user_name, dt, bullets, points):
    """
    Сохраняет новую запись в БД.
    """
    con = sqlite3.connect(settings.DB_PATH)
    c = con.cursor()

    dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(dt))

    rec = (user_name, dt, bullets, points)
    c.execute(f'''
    INSERT INTO {GAME_TABLE}(user_name, dt, bullets, points)
                      VALUES(?,         ?,  ?,       ?)''', rec)
    con.commit()


def get_all_records():
    """
    Получает все записи из БД.
    """
    c = sqlite3.connect(settings.DB_PATH).cursor()
    res = c.execute(f'SELECT id, user_name, dt, bullets, points '
                    f'  FROM {GAME_TABLE} '
                    f' ORDER BY points DESC, bullets, dt').fetchall()
    return res
