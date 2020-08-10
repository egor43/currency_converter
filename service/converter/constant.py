"""
    Константы сервиса конвертации валют
"""
import configparser
from . import data_storage
from . import error


config = configparser.ConfigParser()
if not config.read('configuration.ini'):
    raise error.ServiceError("Не удалось загрузить файл конфигурации")

# Базовая валюта
BASE_CURRENCY = config["CONVERTER"]["BaseCurrency"]

# Хост сервера Redis
REDIS_HOST = config["REDIS"]["Host"]

# Порт сервера Redis
REDIS_PORT = config["REDIS"]["Port"]

# База данных сервера Redis
REDIS_DB = config["REDIS"]["Db"]

# Рабочее хранилище данных
DATA_STORAGE = data_storage.RedisStorage(REDIS_HOST, REDIS_PORT, int(REDIS_DB))
