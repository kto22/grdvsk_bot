# файл с функцией генерации рандомного токена
import random

def random_token():    # простая функция генерации токенов
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return '#'+''.join(random.choice(chars) for _ in range(10))