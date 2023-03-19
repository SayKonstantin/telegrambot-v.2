import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool

@dataclass
class Weather:
    token: str

@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous
    yandex_weather: Weather


def load_config(path: str = None):
    load_dotenv()


    return Config(
        tg_bot=TgBot(
            token=str(os.getenv('BOT_TOKEN')),
            admin_ids=list(map(int, os.getenv('ADMIN'))),
            use_redis=bool(int(os.getenv('REDIS'))),
        ),
        db=DbConfig(
            host=str(os.getenv('DBHOST')),
            password=str(os.getenv('PGPASSWORD')),
            user=str(os.getenv('PGUSER')),
            database=str(os.getenv('DB_NAME'))
        ),
        misc=Miscellaneous(),
        yandex_weather=Weather(
            token=str(os.getenv('WEATHER_TOKEN'))
        )
    )
