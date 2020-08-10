"""
    Модуль предоставляет API сервиса конвертации валют
"""
import json
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
            json - результат конвертации
    """
    try:
        amount = Decimal(amount)
        converted_amount = await converter.convert_currency(amount, currency_from, currency_to)
        result = {"from": currency_from, "to": currency_to,
                  "amount": float(amount),
                  "converted_amount": float(converted_amount)}
        return json.dumps(result)
    except error.ServiceError as exc:
        return json.dumps(exc.to_dict(), ensure_ascii=False)
    except Exception as exc:
        return json.dumps(error.ServiceError(detail_msg=str(exc)).to_dict(), ensure_ascii=False)
