import requests  
import logging  

logger = logging.getLogger(__name__)  

class APIException(Exception):  
    """Исключение для обработки ошибок API"""  
    pass  

class CurrencyConverter:  
    currencies = {"USD", "EUR", "GBP", "RUB", "JPY"}  

    @staticmethod  
    def get_price(base: str, quote: str, amount: float) -> float:  
        if base not in CurrencyConverter.currencies or quote not in CurrencyConverter.currencies:  
            raise APIException(f'Некорректная валюта: {base} или {quote}!')  

        try:  
            response = requests.get(f'https://api.exchangerate-api.com/v4/latest/{base}', timeout=10)  
            response.raise_for_status()  
            data = response.json()  
            logger.info(f'Ответ API: {data}')  
        except requests.RequestException as e:  
            logger.error(f'Ошибка при запросе к API: {e}')  
            raise APIException('Ошибка при получении данных с API.')  

        rate = data['rates'].get(quote)  
        if rate is None:  
            raise APIException('Ставка не найдена!')  

        return rate * amount