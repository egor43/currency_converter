from converter import converter
import asyncio
from decimal import Decimal

loop = asyncio.get_event_loop()

courses_data = {"USD": "73.6376", "EUR": "87.1722"}
#courses_data = {"DKK": "11.6928", "BGN": "44.5425"}

loop.run_until_complete(converter.save_course(courses_data=courses_data))
#loop.run_until_complete(converter.save_course(courses_data=courses_data, delete_old_data=False))


res = loop.run_until_complete(converter.convert_currency(Decimal("1"), "RUB", "USD"))
print(f"RUB to USD: {res}")
res = loop.run_until_complete(converter.convert_currency(Decimal("1"), "USD", "RUB"))
print(f"USD to RUB: {res}")
res = loop.run_until_complete(converter.convert_currency(Decimal("1"), "USD", "EUR"))
print(f"USD to EUR: {res}")
res = loop.run_until_complete(converter.convert_currency(Decimal("1"), "EUR", "EUR"))
print(f"EUR to EUR: {res}")