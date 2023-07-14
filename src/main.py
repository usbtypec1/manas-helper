import pathlib

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import handlers
from config import load_config
from database.base import init_tables
from middlewares import DependencyInjectMiddleware
from repositories import (
    DepartmentRepository, ApplicationRepository,
    RouteRepository
)
from services.departments import init_departments
from tasks import make_snapshot


def main() -> None:
    config_file_path = pathlib.Path(__file__).parent.parent / 'config.toml'
    config = load_config(config_file_path)

    engine = create_engine('sqlite:///../database.db')
    init_tables(engine)
    session_factory = sessionmaker(engine)

    bot = Bot(
        token=config.telegram_bot_token,
        parse_mode=ParseMode.HTML,
    )
    dispatcher = Dispatcher(bot, storage=MemoryStorage())

    handlers.register_handlers(dispatcher)

    department_repository = DepartmentRepository(session_factory)
    application_repository = ApplicationRepository(session_factory)
    route_repository = RouteRepository(session_factory)

    executor.start(
        future=init_departments(department_repository),
        dispatcher=dispatcher,
    )

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        make_snapshot,
        CronTrigger(minute='*'),
        args=(
            bot,
            department_repository,
            application_repository,
            route_repository,
        )
    )
    scheduler.start()

    dispatcher.setup_middleware(
        DependencyInjectMiddleware(
            department_repository=department_repository,
            application_repository=application_repository,
            route_repository=route_repository,
        ),
    )

    executor.start_polling(
        dispatcher=dispatcher,
        skip_updates=True,
    )


if __name__ == '__main__':
    main()
