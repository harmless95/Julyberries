import xmltodict
import httpx
import locale
import asyncio

locale.setlocale(locale.LC_NUMERIC, "")


def convert_number_locale(value):
    try:
        num = locale.atof(value)
        if num.is_integer():
            return int(num)
        else:
            return num
    except:
        return value


BASE_URL = "https://www.cbr.ru/scripts/XML_daily.asp"


async def create_data():
    url = "https://www.cbr.ru/scripts/XML_daily.asp"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    response.encoding = "windows-1251"
    dict_data = xmltodict.parse(response.text)
    for valute in dict_data["ValCurs"]["Valute"]:
        valute["NumCode"] = convert_number_locale(valute["NumCode"])
        valute["Nominal"] = convert_number_locale(valute["Nominal"])
        valute["Value"] = convert_number_locale(valute["Value"])
        valute["VunitRate"] = convert_number_locale(valute["VunitRate"])
    return dict_data


if __name__ == "__main__":
    data = asyncio.run(create_data())
    print(data)
