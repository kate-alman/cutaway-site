import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass
class BotConfig:
    token: str


@dataclass
class RabbitConfig:
    host: str = "localhost"
    port: str = "15672"
    user: str = "guest"
    password: str = "guest"


@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = "postgres"
    database: str = "postgres"


@dataclass
class Config:
    bot: BotConfig = None
    database: DatabaseConfig = None
    rabbitmq: RabbitConfig = None


BASE_DIR = Path(__file__).resolve().parent
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    load_dotenv(dotenv_file)

config_env = os.environ

config = Config(
    bot=BotConfig(
        token=config_env.get("BOT_TOKEN"),
    ),
    database=DatabaseConfig(
        host=config_env.get("POSTGRES_HOST"),
        port=int(config_env.get("POSTGRES_PORT", 5432)),
        user=config_env.get("POSTGRES_USER"),
        password=config_env.get("POSTGRES_PASSWORD"),
        database=config_env.get("POSTGRES_DB"),
    ),
    rabbitmq=RabbitConfig(
        host=config_env.get("RABBITMQ_HOST"),
        port=int(config_env.get("RABBITMQ_PORT")),
        user=config_env.get("RABBITMQ_USER"),
        password=config_env.get("RABBITMQ_PASSWORD"),
    ),
)
