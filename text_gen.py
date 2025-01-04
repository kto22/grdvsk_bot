# файл генерации текста
from langchain_ollama import ChatOllama    # импортируем фреймворк взаимодействия с нейронками
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from deep_translator import GoogleTranslator    # импортим переводчик


async def generate_text(model, message):    # функция генерации текста

    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    llm = ChatOllama(    # тут в олламе объявляем модель
        model=model,
        temperature=0.75,
        max_tokens=2000,
        top_p=1,
        callback_manager=callback_manager,
        verbose=True,
    )
    message = message.lower().replace('мем', 'шутку')    # заменяем мем на шутку, ибо от нейронки нам нужно только шутку
    message = GoogleTranslator(source='auto', target='en').translate(message)    # переводим язык сообщения на английский, ибо нейронка лучше всего работает именно с ним
    history = [    # тут контекст задаём, просим, чтоб нейронка сделала одну короткую шутку
        {
            "role": "system",
            "content": "You must to create one very short joke (less than 10 words)."
        },
        {
            "role": "user",
            "content": f"{message}. You must to create one very short joke (less than 10 words)."
        }
    ]

    msg = llm.invoke(history)    # тут генерим шутку
    return GoogleTranslator(source='auto', target='ru').translate(msg.content)    # тут возвращем полученную шутку, переведя её на русский