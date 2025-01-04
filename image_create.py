# файл добавления текста на изображение
from PIL import Image, ImageDraw, ImageFont    # импорт библиотеки для работы с изображениями
from random import randint


async def add_text_to_image(text, font_path, font_size, text_color, text_position, chat_id):

    new_text = ''                   # это простейший алгоритм переноса строки, чтобы ответ нейронки не выходил через правый край изображения
    for i in range(32, len(text), 32):
        new_text = new_text + text[i-32:i]+' -\n'
    new_text = new_text + text[i::]
    print(new_text)
    n = i//32+1


    image = Image.open(f'images/{randint(1,4)}.jpg')
    image = image.resize((480, 480))    # изменяем его размер под свой стандарт
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(font_path, font_size)    # это шрифт для текста
    font1 = ImageFont.truetype(font_path, font_size*n)    # это шрифт для белого фона текста
    bbox = draw.textbbox(text_position, text, font=font1)    # рисуем фон
    draw.rectangle(bbox, fill="white")
    draw.text(text_position, new_text, font=font, fill=text_color)    # добавляем текст

    image.save(f'images/{chat_id}.jpg')    # сохраняем изображение пользователя с id чата в названии


