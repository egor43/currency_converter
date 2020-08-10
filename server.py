"""
    Модуль серверной части сервиса конвертации валют
"""
from aiohttp import web
import logging
import logging.config
import service_api

async def convert_handler(request):
    """
        Обработчик запроса конвертации
        Params:
            request - входящий запрос
        Return:
            Response - ответ на запрос
    """
    logger.info(request.url)
    currency_from = request.rel_url.query["from"]
    currency_to = request.rel_url.query["to"]
    amount = request.rel_url.query["amount"]
    result = await service_api.convert(currency_from, currency_to, amount)
    return web.json_response(data=result)


async def database_handler(request):
    """
        Обработчик запроса обновления данных
        Params:
            request - входящий запрос
        Return:
            Response - ответ на запрос
    """
    logger.info(request.url)
    merge_mode = request.rel_url.query["merge"]
    courses_data = await request.json()
    logger.debug(courses_data)
    result = await service_api.merge(merge_mode, courses_data)
    return web.json_response(data=result)


logging.config.fileConfig("logger.conf")
logger = logging.getLogger("ConverterService.server")

app = web.Application()
app.add_routes([web.get('/convert', convert_handler),
                web.post('/database', database_handler)])

if __name__ == '__main__':
    web.run_app(app)
