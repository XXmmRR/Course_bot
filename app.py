import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
import config
from handlers.start import start_router
from handlers.main_menu import menu_router


logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    )

storage = MemoryStorage()
# storage = RedisStorage2()
dp = Dispatcher(storage=storage)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    dp.include_router(start_router)
    dp.include_router(menu_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
