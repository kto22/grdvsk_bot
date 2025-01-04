import sqlite3   #тут импортируем библиотеку для работы с БД на sqlite
from randomizer import random_token    # импортируем генерацию токена

connection = sqlite3.connect('database.db')   #тут подключаемся к БД
cursor = connection.cursor()


def recreate_table():    # функция для пересоздания главной таблицы
    cursor.execute('DROP TABLE IF EXISTS users')
    connection.commit()
    cursor.execute(f'''
            CREATE TABLE users (
            token TEXT,
            chat_id TEXT,
            is_authorized BOOLEAN,
            model TEXT
            )
            ''')
    connection.commit()

    for _ in range(100):
        cursor.execute('INSERT INTO users (token, chat_id, is_authorized, model) VALUES (?,?,?,?)', (random_token(), '0', False, 'phi3'))
    connection.commit()


async def get_model(chat_id):    # функция получения модели из БД
    cursor.execute('SELECT * FROM users WHERE chat_id=?', (chat_id,))
    model = cursor.fetchone()[3]
    return model


async def update_model(chat_id, model):    # функция обновления модели в БД
    cursor.execute("UPDATE users SET model = ? WHERE chat_id = ?", (model, chat_id))
    connection.commit()
    return 0


async def is_user_added(chat_id):    # функция проверки наличия пользователя в БД
    cursor.execute('SELECT COUNT(*) FROM users WHERE chat_id=?', (chat_id,))
    count = cursor.fetchone()[0]
    return count > 0


async def is_token_authorized(token):    # функция проверки занятости токена
    cursor.execute('SELECT * FROM users WHERE token=?', (token,))
    if not cursor.fetchone()[2]:
        return False
    return True


async def auth_user(chat_id, token):    # функция авторизации пользователя
    cursor.execute('UPDATE users SET is_authorized = 1, chat_id = ? WHERE token = ?', (chat_id, token))
    connection.commit()


async def is_token_valid(token):    # функция проверки наличия такого токена в БД
    cursor.execute('SELECT COUNT(*) FROM users WHERE token = ?', (token,))
    count = cursor.fetchone()[0]
    print(count)
    return count > 0

