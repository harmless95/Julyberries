from core.config import setting


def formate_save(data_valute):
    char_code_save = setting.valute_conf.valute  # базовая валюта, например 'USD'
    for valute in data_valute["ValCurs"]["Valute"]:
        if valute.get("CharCode") == char_code_save:
            value_str = valute.get("Value").replace(",", ".")
            nominal = valute.get("Nominal", 1)
            rate = float(value_str) / nominal  # курс за 1 единицу валюты
            return rate
    return None
