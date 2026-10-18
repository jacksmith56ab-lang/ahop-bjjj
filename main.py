from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage

from config import load_settings
from database import init_database, make_engine, make_session_factory
from handlers.admin import make_admin_router
from handlers.user import make_user_router
from keyboards import ICON_SLOTS, ICONS
from services.store import get_setting, initialize_settings


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    settings = load_settings()
    engine = make_engine(settings.database_path)
    await init_database(engine)
    session_factory = make_session_factory(engine)
    await initialize_settings(session_factory)
    async with session_factory() as session:
        for slot in ICON_SLOTS:
            icon = await get_setting(session, f"icon_{slot}", "")
            if icon:
                ICONS[slot] = icon

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(),
    )
    try:
        me = await bot.get_me()
        await bot.set_my_commands(
            [
                BotCommand(command="start", description="Открыть магазин"),
                BotCommand(command="admin", description="Админ-панель"),
            ]
        )
        dispatcher = Dispatcher(storage=MemoryStorage())
        dispatcher.include_router(make_admin_router(session_factory, settings.admin_id))
        dispatcher.include_router(
            make_user_router(session_factory, settings.admin_id, me.username or "")
        )
        logging.getLogger("standoff2_bot").info("Bot @%s started; SQLite initialized.", me.username)
        await dispatcher.start_polling(
            bot,
            allowed_updates=dispatcher.resolve_used_update_types(),
            close_bot_session=False,
        )
    finally:
        await bot.session.close()
        await engine.dispose()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
