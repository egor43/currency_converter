"""
    Модуль работы с хранилищами данных
"""
import asyncio
import aioredis
from . import error
from decimal import Decimal


class MetaSingleton(type):
    """
        Метакласс синглтона
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class RedisStorage(metaclass=MetaSingleton):
    """
        Хранилище данных на основе Redis
    """
    def __init__(self, host, port, db):
        """
            Инициализация хранилища данных
            Params:
                host - хост сервера
                port - порт сервера
                db - база даннных
        """
        loop = asyncio.get_event_loop()
        self._redis = loop.run_until_complete(RedisStorage._create_redis_pool(host, port, db))

    @staticmethod
    async def _create_redis_pool(host, port, db):
        """
            Создание пула подключений к серверу Redis
            Params:
                host - хост сервера
                port - порт сервера
                db - база даннных
            Return:
                redis_pool - пул подключений к серверу Redis
        """
        try:
            pool = await aioredis.create_redis_pool(address=(host, port), db=db)
            await pool.ping()
            return pool
        except Exception as exc:
            raise error.ServiceError(f"При создании подключения к серверу Redis возникла проблема: {exc}")

    async def update_course(self, base_currency, target_currency_data):
        """
            Обновление курса валюты.
            Params:
                base_currency - базовая валюта
                target_currency_data - курсы валют
                    key - код названия валюты
                    value - курс указанной валюты
                    Пример: {"USD": "73.6376", "EUR": "87.1722"}
            Return:
                True - если процесс обновления прошел успешно, иначе генерируется ошибка
        """
        try:
            transaction = self._redis.multi_exec()
            transaction.hmset_dict(base_currency, target_currency_data)
            await transaction.execute()
            return True
        except Exception as exc:
            raise error.ServiceError(f"При обновлении данных возникла ошибка: {exc}")

    async def save_course(self, base_currency, target_currency_data):
        """
            Сохранение курса валюты с предварительной очисткой старых данных.
            Params:
                base_currency - базовая валюта
                target_currency_data - курсы валют
                    key - код названия валюты
                    value - курс указанной валюты
                    Пример: {"USD": "73.6376", "EUR": "87.1722"}
            Return:
                True - если процесс сохранения прошел успешно, иначе генерируется ошибка
        """
        try:
            transaction = self._redis.multi_exec()
            transaction.delete(base_currency)
            transaction.hmset_dict(base_currency, target_currency_data)
            await transaction.execute()
            return True
        except Exception as exc:
            raise error.ServiceError(f"При сохранении данных возникла ошибка: {exc}")

    async def get_course(self, base_currency, target_currency):
        """
            Получение курса валют из БД
            Params:
                base_currency - базовая валюта
                target_currency - валюта для которой необходимо вернуть текущий курс
            Return:
                Decimal - текущий курс для указанной валюты
        """
        try:
            data = await self._redis.hget(base_currency, target_currency, encoding="utf-8")
            result = Decimal(data) if data else Decimal()
            return result
        except Exception as exc:
            raise error.ServiceError(f"При получении данных возникла ошибка {exc}")
