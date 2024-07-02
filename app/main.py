from services.seller_bot import TelegramBot
from alembic.config import Config
from alembic import command


alembic_cfg = Config("alembic.ini")
command.upgrade(alembic_cfg, "base")

if __name__ == '__main__':
    seller_bot = TelegramBot()
    seller_bot.run()
