# файл обработки сообщений
from aiogram import F, Router, types    # импортируем всё нужное из aiogram
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton

import image_create    # импортируем файлик для добавления текста на изображение
import data_func    # файлик для работы с базой данных
import text_gen    # файлик с функцией генерации текста


router = Router()    # объявляем роутер


@router.message(F.text == '/start')    # вызывается по команде /start
async def start(message: Message):    # функция обработки команды старт
    chat_id = message.chat.id
    if not await data_func.is_user_added(chat_id):    # проверка отсутствия авторизованности пользователя
        await message.answer('Привет! С помощью этого бота ты можешь сгенерировать мем!\n'
                             'Но сначала введи свой уникальный токен!')
        return 0


@router.message(F.text[0] == '#')    # вызывается, если первый символ в сообщении это решётка
async def auth(message: Message):    # функция аутентификации пользователя
    chat_id = message.chat.id
    token = message.text
    if not await data_func.is_token_valid(token):    # проверка верности токена
        await message.answer('Неверный токен!')
        return 0
    if await data_func.is_user_added(chat_id):    # проверка уже наличия пользователя в БД
        await message.answer('Вы уже авторизованы!')
        return 0
    if await data_func.is_token_authorized(token):    # проверка на то, занят ли токен кем-то другим
        await message.answer('Этот токен уже занят!')
        return 0

    await data_func.auth_user(chat_id, token)    # добавления юзера в БД
    await message.answer('Вы успешно авторизовались!')


@router.message(F.text == '/model')    # вызывается по команде /model
async def model_sel(message: Message):    # функция выбора модели
    chat_id = message.chat.id
    if not await data_func.is_user_added(chat_id):    # проверка авторизованности юзера
        await start(message)
        return 0

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Llava", callback_data="llava"),
            InlineKeyboardButton(text="Phi-3", callback_data="phi")
        ]
    ])
    await message.answer("Выберите модель, которую хотите использовать:", reply_markup=inline_keyboard)


@router.callback_query(lambda c: c.data == "llava")
async def button1_callback_handler(callback_query: types.CallbackQuery):    # функция обновления модели в БД на ллаву
    await data_func.update_model(callback_query.message.chat.id, 'llava')
    await callback_query.answer('Вы выбрали модель Llava')


@router.callback_query(lambda c: c.data == "phi")
async def button2_callback_handler(callback_query: types.CallbackQuery):    # функция обновления модели в БД фи-3
    await data_func.update_model(callback_query.message.chat.id, 'phi3')
    await callback_query.answer('Вы выбрали модель Phi-3')


@router.message()
async def any_message(message: Message):    # функция обработки запросов к нейронке
    if not await data_func.is_user_added(message.chat.id):    # проверка авторизованности юзера
        await start(message)
        return 0
    chat_id = message.chat.id
    print(message.text)
    model = await data_func.get_model(chat_id)    # получение выбранной пользователем модели из БД
    msg = await text_gen.generate_text(model, message.text)    # получение сгенерированного текста
    await image_create.add_text_to_image(msg,    # создание изображения
                      'fonts/Andy_Bold_0.otf', 32, (0, 0, 0), (0, 255, 0), chat_id)
    photo = FSInputFile(f'images/{chat_id}.jpg')
    await message.answer_photo(photo=photo)    # отправка изображения


