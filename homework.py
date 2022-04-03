import logging
import os
import requests
import sys
import telegram
import time


from dotenv import load_dotenv


load_dotenv()


PRACTICUM_TOKEN = os.getenv('MY_TOKEN')
TELEGRAM_TOKEN = os.getenv('TG_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


def send_message(bot, message):
    """Отправка сообщения."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.info('Сообщение успешно отправлено')
    except Exception:
        message = 'Произошел сбой при отправке сообщения'
        logger.error(message)
        bot.send_message(TELEGRAM_CHAT_ID, message)


def get_api_answer(current_timestamp):
    """Получает временную метку.
    Делает запрос к единственному эндпоинту API-сервиса
    и возвращает ответ API.
    """
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    response = requests.get(url=ENDPOINT, headers=HEADERS, params=params)
    try:
        response
        if response.status_code == 200:
            return response.json()
        message = 'Эндпоинт недоступен'
        logger.error(message)
        raise ValueError(message)
    except telegram.TelegramError:
        message = 'Наблюдаются сбои при запросе к эндпоинту'
        logger.error(message)


def check_response(response):
    """Получает ответ API.
    Возвращает список домашних работ из ответа API.
    """
    homeworks_list = response['homeworks']
    if not isinstance(response, dict):
        raise ValueError('Ответ API представлен не в виде словаря')
    if not bool(response):
        raise ValueError('Ответ API пришел в виде пустого словаря')
    if not isinstance(homeworks_list, list):
        raise ValueError('Домашние задания представлены не в виде списка')
    if 'homeworks' not in response:
        return False
    return homeworks_list


def parse_status(homework):
    """Получает один элемент из списка домашних работ.
    Возвращает статус этой работы.
    """
    homework_name = homework['homework_name']
    homework_status = homework['status']
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    try:
        all((homework_name, homework_status))
        if homework_status in HOMEWORK_VERDICTS:
            verdict = HOMEWORK_VERDICTS[homework_status]
            message = (f'Изменился статус проверки работы "{homework_name}". '
                       f'{verdict}')
            return message
        message = f'Статус {homework_status} недокументирован'
        logger.error(message)
        bot.send_message(TELEGRAM_CHAT_ID, message)
        raise ValueError(message)
    except Exception:
        message = 'Ключи "homework_name" и "status" в списке отсутствуют'
        logger.error(message)
        bot.send_message(TELEGRAM_CHAT_ID, message)
        raise ValueError(message)


def check_tokens() -> bool:
    """Проверяет доступность переменных окружения."""
    return all((PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID))


def main():
    """Основная логика работы бота."""
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    initial_message = ''
    if check_tokens() is False:
        logger.critical('Переменные окружения отсутствуют')
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homework = check_response(response)
            if homework is not False:
                current_homework = homework[0]
                message = parse_status(current_homework)
            else:
                message = 'В списке отсутствует ключ "homeworks"'
                logger.error(message)
            if message == initial_message:
                pass
            else:
                initial_message = message
                bot.send_message(TELEGRAM_CHAT_ID, initial_message)
            current_timestamp = int(time.time())
            time.sleep(RETRY_TIME)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            bot.send_message(TELEGRAM_CHAT_ID, message)
            time.sleep(RETRY_TIME)
        else:
            pass


if __name__ == '__main__':
    logging.basicConfig(
        filename='main.log',
        format='%(asctime)s [%(levelname)s] %(message)s'
    )
    main()
