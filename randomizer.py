import random

def random_token():
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return '#'+''.join(random.choice(chars) for _ in range(10))