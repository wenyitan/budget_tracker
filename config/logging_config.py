import logging as logger
from config.env_config import env, app

log_filename = f'{app}.log' if env == "prod" else f'{app}_{env}.log'

logger.basicConfig(
    filename=f"logs/{log_filename}",
    level=logger.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)