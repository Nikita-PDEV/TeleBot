import telebot  
import logging  
from config import TOKEN
print(TOKEN)  
from extensions import CurrencyConverter, APIException  

# Настройка логирования  
logging.basicConfig(  
    level=logging.DEBUG,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  
    handlers=[  
        logging.FileHandler("bot.log", mode='a', encoding='utf-8'),  
        logging.StreamHandler()  
    ]  
)  

logger = logging.getLogger(__name__)  
bot = telebot.TeleBot(TOKEN)  

@bot.message_handler(commands=['start'])  
def send_welcome(message):  
    text = """Привет! Я бот для конвертации валют.  
    
    Для помощи по использованию бота нажми /help."""  
    bot.reply_to(message, text)  

@bot.message_handler(commands=['help'])  
def send_help(message):  
    text = """Формат: например, USD EUR 100, "валюта" "валюта" "число"  
    Число должно быть положительным.  
    Воспользуйся командой /values для просмотра списка доступных валют."""  
    bot.reply_to(message, text)  

@bot.message_handler(commands=['values'])  
def available_currencies(message):  
    """Команда для получения списка доступных валют."""  
    text = 'Доступные валюты: ' + ', '.join(CurrencyConverter.currencies)  
    bot.reply_to(message, text)  

@bot.message_handler(content_types=['text'])  
def convert_currency(message: telebot.types.Message):  
    logger.info(f"Получен запрос на конвертацию: {message.text}")  

    try:  
        base, quote, amount = message.text.split(' ')  
        amount = float(amount)  

        if amount <= 0:  
            raise APIException('Число должно быть положительным.')  

        price = CurrencyConverter.get_price(base.upper(), quote.upper(), amount)  
        text = f'Цена {amount} {base.upper()} в {quote.upper()} составляет {price:.2f}'  
        bot.reply_to(message, text)  

    except ValueError:  
        logger.error("Неправильный формат запроса.")  
        bot.reply_to(message, 'Неправильный формат. Попробуйте: валюта1 валюта2 число')  
    except APIException as e:  
        logger.error(f'Ошибка API: {e}')  
        bot.reply_to(message, f'Ошибка: {e}')  
    except Exception as e:  
        logger.error(f'Неизвестная ошибка: {e}')  
        bot.reply_to(message, 'Произошла ошибка. Повторите попытку.')  

if __name__ == '__main__':  
    logger.info("Бот запущен и работает")  
    bot.polling(none_stop=True)  