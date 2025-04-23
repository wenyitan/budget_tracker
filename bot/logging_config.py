import logging as logger

logger.basicConfig(
    filename='bot.log',
    level=logger.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)