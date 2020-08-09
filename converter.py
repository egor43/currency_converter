"""
    Модуль реализующий функционал конвертации валюты
"""
import constant
import error
from decimal import Decimal
from decimal import ROUND_HALF_UP


def convert_currency(amount, currency_from, currency_to):
    """
        Конвертация валют
        Params:
            amount - количество денежных единиц, подвергаемых конвертации
            currency_from - валюта из которой необходимо преобразовать
            currency_to - валюта в которую необходимо преобразовать
        Result:
            Decimal - сконвертированное округленное значение
    """
    if currency_from == constant.BASE_CURRENCY:
        course = get_course_value(currency_to)
        result = amount / course
    elif currency_to == constant.BASE_CURRENCY:
        course = get_course_value(currency_from)
        result = amount * course
    else:
        # Если ни одна из указанных валют не является базовой, нужно привести денежные единицы в базовую валюту
        amount = convert_currency(amount, currency_from, constant.BASE_CURRENCY)
        course = get_course_value(currency_to)
        result = amount / course
    # Возвращаем округленное значение по формату ЦБ РФ
    return result.quantize(Decimal("1.0000"), ROUND_HALF_UP)


def get_course_value(currency):
    """
        Возвращает значение курса указанной валюты
        Params:
            currency - валюта, курс которой необходимо вренуть
        Result:
            Decimal - значение курса валюты
    """
    course = constant.DATA_STORAGE.get_course(constant.BASE_CURRENCY, currency)
    if not course:
        raise error.ConverterError(f"Не удалось получить курс валюты {currency}")
    return course