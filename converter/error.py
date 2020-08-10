"""
    Модуль содержит набор переопределенных классов ошибок сервиса
"""


class ServiceError(Exception):
    """
        Базовый класс ошибок сервиса
    """
    def __init__(self, detail_msg="Ошибка в работе сервиса", error_code=0):
        """
            Инициализация базового класса исключения
            Params:
                detail_msg - описание ошибки
                error_code - код ошибки
        """
        self.detail_msg = detail_msg
        self.error_code = error_code
        super().__init__(detail_msg)
    
    def to_dict(self):
        """
            Преобразование объекта ошибки в словарь
            Return:
                dict - представление объекта в виде словаря
        """
        return {"error_code": self.error_code, "detail_msg": self.detail_msg}


class ConverterError(ServiceError):
    """
        Базовый класс ошибок конвертации
    """
    def __init__(self, detail_msg="Ошибка конвертации", error_code=1):
        """
            Инициализация класса исключения ошибки конвертации
            Params:
                detail_msg - описание ошибки
                error_code - код ошибки
        """
        super().__init__(detail_msg, error_code)
