"""
    Модуль предоставляет API сервиса конвертации валют
"""
from decimal import Decimal
from converter import converter
from converter import error


async def convert(currency_from, currency_to, amount):
    """
        Конвертация валюты
        Params:
            currency_from - валюта из которой необходимо преобразовать
            currency_to - валюта в которую неоходимо преобразовать
            amount - количество конвертируемых денежных единиц
        Return:
            dict - результат конвертации
    """
    try:
        amount = Decimal(amount)
        converted_amount = await converter.convert_currency(amount, currency_from, currency_to)
        result = {"from": currency_from, "to": currency_to,
                  "amount": float(amount),
                  "converted_amount": float(converted_amount)}
        return result
    except error.ServiceError as exc:
        return exc.to_dict()
    except Exception as exc:
        return error.ServiceError(detail_msg=str(exc)).to_dict()


async def merge(merge_mode, data):
    """
        Добавление записей в хранилище данных
        Params:
            merge_mode - режим добавления данных
                "0" - полная замена всех данных в хранилище
                "1" - обновление данных
            data - данные для обновления
                key - код названия валюты
                value - курс указанной валюты
                Пример: {"USD": "73.6376", "EUR": "87.1722"}
        Return:
            dict - результат добавления
    """
    try:
        if merge_mode == "0":
            save_status = await converter.save_course(data, save_old_data=False)
        elif merge_mode == "1":
            save_status = await converter.save_course(data, save_old_data=True)
        else:
            raise error.ServiceError(detail_msg=f"Некорректный режим добавления данных: {merge_mode}")
        return {"result": save_status}
    except error.ServiceError as exc:
        return exc.to_dict()
    except Exception as exc:
        return error.ServiceError(detail_msg=str(exc)).to_dict()
