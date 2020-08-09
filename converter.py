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


def save_course(courses_data, delete_old_data=True):
    """
        Сохранение курсов валют
        Params:
            courses_data - данные о курсах валют, которые требуется сохранить
                key - код названия валюты
                value - курс указанной валюты
                Пример: {"USD": "73.6376", "EUR": "87.1722"}
            delete_old_data - логическое значение необходимости очистки старых значений
    """
    if delete_old_data:
        constant.DATA_STORAGE.save_course(constant.BASE_CURRENCY, courses_data)
    else:
        constant.DATA_STORAGE.update_course(constant.BASE_CURRENCY, courses_data)
