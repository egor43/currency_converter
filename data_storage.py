"""
    Модуль работы с хранилищами данных
"""
import redis
import error
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
                host - хост сервера Redis
                port - порт сервера Redis
                db - номер базы
        """
        try:
            self._redis = redis.Redis(host=host, port=port, db=db)
            self._redis.ping()
        except Exception as exc:
            raise error.ServiceError(f"Не удалось подключиться к серверу Redis: {exc}")

    def update_course(self, base_currency, target_currency_data):
        """
            Обновление курса валюты.
            Params:
                base_currency - базовая валюта
                target_currency_data - курсы валют
                    key - код названия валюты
                    value - курс указанной валюты
                    Пример: {"USD": "73.6376", "EUR": "87.1722"}
        """
        try:
            with self._redis.pipeline() as pipe:
                pipe.multi()
                pipe.hmset(base_currency, target_currency_data)
                pipe.execute()
        except Exception as exc:
            raise error.ServiceError(f"При обновлении данных возникла ошибка: {exc}")

    def save_course(self, base_currency, target_currency_data):
        """
            Сохранение курса валюты с предварительной очисткой старых данных.
            Params:
                base_currency - базовая валюта
                target_currency_data - курсы валют
                    key - код названия валюты
                    value - курс указанной валюты
                    Пример: {"USD": "73.6376", "EUR": "87.1722"}
        """
        try:
            with self._redis.pipeline() as pipe:
                pipe.multi()
                pipe.delete(base_currency)
                pipe.hmset(base_currency, target_currency_data)
                pipe.execute()
        except Exception as exc:
            raise error.ServiceError(f"При сохранении данных возникла ошибка: {exc}")

    def get_course(self, base_currency, target_currency):
        """
            Получение курса валют из БД
            Params:
                base_currency - базовая валюта
                target_currency - валюта для которой необходимо вернуть текущий курс
            Return:
                Decimal - текущий курс для указанной валюты
        """
        try:
            binary_data = self._redis.hget(base_currency, target_currency)
            result = Decimal(binary_data.decode("utf-8")) if binary_data else Decimal()
            return result
        except Exception as exc:
            raise error.ServiceError(f"При получении данных возникла ошибка {exc}")
