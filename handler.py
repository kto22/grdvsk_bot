from aiogram import F, Router, types
from aiogram.types import Message, InputFile, FSInputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import image_create
import data_func
import text_gen


router = Router()


@router.message(F.text == '/start')
async def start(message: Message):
    chat_id = message.chat.id
    if not await data_func.is_user_added(chat_id):
        await message.answer('Привет! С помощью этого бота ты можешь сгенерировать мем!\n'
                             'Но сначала введи свой уникальный токен!')
        return 0


@router.message(F.text[0] == '#')
async def auth(message: Message):
    chat_id = message.chat.id
    token = message.text
    if not await data_func.is_token_valid(token):
        await message.answer('Неверный токен!')
        return 0
    if await data_func.is_user_added(chat_id):
        await message.answer('Вы уже авторизованы!')
        return 0
    if await data_func.is_token_authorized(token):
        await message.answer('Этот токен уже занят!')
        return 0

    await data_func.auth_user(chat_id, token)
    await message.answer('Вы успешно авторизовались!')

@router.message(F.text == '/model')
async def model_sel(message: Message):
    chat_id = message.chat.id
    if not await data_func.is_user_added(chat_id):
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
async def button1_callback_handler(callback_query: types.CallbackQuery):
    await data_func.update_model(callback_query.message.chat.id, 'llava')
    await callback_query.answer('Вы выбрали модель Llava')


@router.callback_query(lambda c: c.data == "phi")
async def button2_callback_handler(callback_query: types.CallbackQuery):
    await data_func.update_model(callback_query.message.chat.id, 'phi3')
    await callback_query.answer('Вы выбрали модель Phi-3')


@router.message()
async def any_message(message: Message):
    if not await data_func.is_user_added(message.chat.id):
        await start(message)
        return 0
    chat_id = message.chat.id
    print(message.text)
    model = await data_func.get_model(chat_id)
    msg = await text_gen.generate_text(model, message.text)
    await image_create.add_text_to_image(msg,
                      'fonts/Andy_Bold_0.otf', 32, (0, 0, 0), (0, 255, 0), chat_id)
    photo = FSInputFile(f'images/{chat_id}.jpg')
    await message.answer_photo(photo=photo)
    #await message.answer(msg)


