from PIL import Image, ImageDraw, ImageFont
from random import randint



async def add_text_to_image(text, font_path, font_size, text_color, text_position, chat_id):

    new_text = ''
    for i in range(32, len(text), 32):
        print(i)
        new_text = new_text + text[i-32:i]+' -\n'
    new_text = new_text + text[i::]
    print(new_text)
    n = i//32+1


    image = Image.open(f'images/{randint(1,4)}.jpg')
    image = image.resize((480, 480))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(font_path, font_size)
    font1 = ImageFont.truetype(font_path, font_size*n)
    bbox = draw.textbbox(text_position, text, font=font1)
    draw.rectangle(bbox, fill="white")
    draw.text(text_position, new_text, font=font, fill=text_color)

    image.save(f'images/{chat_id}.jpg')


