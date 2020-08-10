"""
    Модуль серверной части сервиса конвертации валют
"""
from aiohttp import web
from decimal import Decimal
from converter import converter

async def convert_handler(request):
    """
        Обработчик запроса конвертации
        Params:
            request - входящий запрос
        Return:
            Response - ответ на запрос
    """
    currency_from = request.rel_url.query["from"]
    currency_to = request.rel_url.query["to"]
    amount = request.rel_url.query["amount"]
    result = await converter.convert_currency(Decimal(amount), currency_from, currency_to)
    return web.Response(status=200, text=str(result))


async def database_handler(request):
    """
        Обработчик запроса обновления данных
        Params:
            request - входящий запрос
        Return:
            Response - ответ на запрос
    """
    merge_status = request.rel_url.query["merge"]
    courses_data = await request.json()
    await converter.save_course(courses_data, True if merge_status == "1" else False)
    return web.Response(status=200, text="Ok")


app = web.Application()
app.add_routes([web.get('/convert', convert_handler),
                web.post('/database', database_handler)])

if __name__ == '__main__':
    web.run_app(app)
