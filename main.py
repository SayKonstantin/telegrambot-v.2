import os


def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "django_project.telegrambot.telegrambot.settings"
    )
    os.environ.update(
        {
            "DJANGO_ALLOW_ASYNC_UNSAFE": "true"
        }
    )
    import django
    django.setup()


if __name__ == "__main__":
    from tgbot.misc.logger import logger

    try:
        setup_django()
        logger.info('Django активирован')
    except Exception:
        raise logger.error('проблемы с установкой Django')

    from aiogram import executor
    from tgbot import middlewares
    from tgbot.handlers import dp

    try:
        logger.info('Бот работает')
        middlewares.setup(dp)
        executor.start_polling(dp, skip_updates=True)
    except Exception as error:
        raise logger.error(f'ПРОБЛЕМА {error=}! Бот остановлен')
