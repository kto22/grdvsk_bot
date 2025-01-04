from langchain_ollama import ChatOllama
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from deep_translator import GoogleTranslator


async def generate_text(model, message):

    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    llm = ChatOllama(
        model=model,
        temperature=0.75,
        max_tokens=2000,
        top_p=1,
        callback_manager=callback_manager,
        verbose=True,
    )
    message = message.replace('мем', 'шутку')
    message = GoogleTranslator(source='auto', target='en').translate(message)
    history = [
        {
            "role": "system",
            "content": "You must to create one very short joke (less than 10 words)."
        },
        {
            "role": "user",
            "content": f"{message}. You must to create one very short joke (less than 10 words)."
        }
    ]

    msg = llm.invoke(history)
    return GoogleTranslator(source='auto', target='ru').translate(msg.content)