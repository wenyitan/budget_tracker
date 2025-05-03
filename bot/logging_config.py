import logging as logger
from bot.config import env

log_filename = 'bot.log' if env == "prod" else f'bot_{env}.log'

logger.basicConfig(
    filename=log_filename,
    level=logger.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)