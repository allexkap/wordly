import asyncio
import os
from collections import Counter
from typing import Iterable

from aiogram import Bot, Dispatcher, html
from aiogram.types import Message

with open('five.txt') as file:
    words = file.read().split('\n')

TOKEN = os.environ['BOT_TOKEN']
dp = Dispatcher()


def filter5(pattern: str, words: Iterable[str]) -> Iterable[str]:
    parts = pattern.split()
    if len(parts) < 5:
        raise ValueError('not enough positional letters')

    letters = [(ch.startswith('+'), ch[1:]) for ch in parts[:5]]

    somewhere, nowhere = Counter(), set()
    for part in parts[5:]:
        if part.startswith('?'):
            somewhere.update(part[1:])
        elif part.startswith('-'):
            nowhere.update(part[1:])
        else:
            pass  # warning

    return filter(
        lambda word: all(ch not in word for ch in nowhere)
        and all(
            all((ch1 == ch2) == eq for ch1 in chs)
            for (eq, chs), ch2 in zip(letters, word)
        )
        and max((somewhere - Counter(word)).values(), default=0) == 0,
        words,
    )


@dp.message()
async def default_handler(message: Message) -> None:
    if (pattern := message.text) is None:
        return
    try:
        text = ' '.join(filter5(pattern, words))
        text = text[:1024] + ('...' if len(text) > 1024 else '')
        await message.answer(html.code(text), parse_mode='html')
    except ValueError as err:
        await message.answer(str(err))


if __name__ == '__main__':
    bot = Bot(token=TOKEN)
    asyncio.run(dp.start_polling(bot))
