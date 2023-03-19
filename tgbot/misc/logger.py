import logging
from logging import Logger

logging.basicConfig(
    level=logging.INFO,
    encoding='utf-8',
    format="|\t%(asctime)s – [%(levelname)s]: %(message)s. "
           "Исполняемый файл – '%(filename)s': функция – '%(funcName)s'(%(lineno)d)",
)
logger: Logger = logging.getLogger(__name__)
