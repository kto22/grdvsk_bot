import sqlite3   #тут импортируем библиотеку для работы с БД
from randomizer import random_token

connection = sqlite3.connect('database.db')   #тут подключаемся к БД
cursor = connection.cursor()
print("connected to database successfully")

def recreate_table():
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
    print('table users recreated successfully')


async def get_model(chat_id):
    cursor.execute('SELECT * FROM users WHERE chat_id=?', (chat_id,))
    model = cursor.fetchone()[3]
    return model


async def update_model(chat_id, model):
    cursor.execute("UPDATE users SET model = ? WHERE chat_id = ?", (model, chat_id))
    connection.commit()
    print('model updated successfully')
    return 0


async def is_user_added(chat_id):
    cursor.execute('SELECT COUNT(*) FROM users WHERE chat_id=?', (chat_id,))
    count = cursor.fetchone()[0]
    return count > 0


async def is_token_authorized(token):
    cursor.execute('SELECT * FROM users WHERE token=?', (token,))
    if not cursor.fetchone()[2]:
        return False
    return True


async def auth_user(chat_id, token):
    cursor.execute('UPDATE users SET is_authorized = 1, chat_id = ? WHERE token = ?', (chat_id, token))
    connection.commit()


async def is_token_valid(token):
    cursor.execute('SELECT COUNT(*) FROM users WHERE token = ?', (token,))
    count = cursor.fetchone()[0]
    print(count)
    return count > 0

