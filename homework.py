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


def send_message(bot, message):
    """Отправка сообщения."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.info('Сообщение успешно отправлено')
    except telegram.TelegramError:
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
    try:
        response = requests.get(url=ENDPOINT, headers=HEADERS, params=params)
        if response.status_code == 200:
            return response.json()
        message = 'Эндпоинт недоступен'
        logger.error(message)
        raise ValueError(message)
    except telegram.TelegramError:
        message = 'Наблюдаются сбои при запросе к эндпоинту'
        logger.error(message)
        raise KeyError


def check_response(response):
    """Получает ответ API.
    Возвращает список домашних работ из ответа API.
    """
    homeworks_list = response['homeworks']
    if not isinstance(homeworks_list, list):
        message = 'Домашние задания представлены не в виде списка'
        logger.error(message)
        raise ValueError(message)
    if 'homeworks' not in response:
        message = 'В списке отсутствует ключ "homeworks"'
        logger.error(message)
        raise ValueError(message)
    return homeworks_list


def parse_status(homework):
    """Получает один элемент из списка домашних работ.
    Возвращает статус этой работы.
    """
    homework_name = homework['homework_name']
    homework_status = homework['status']
    if homework_status not in HOMEWORK_VERDICTS:
        message = f'Статус {homework_status} недокументирован'
        logger.error(message)
        raise ValueError
    verdict = HOMEWORK_VERDICTS[homework_status]
    message = (f'Изменился статус проверки работы "{homework_name}". '
               f'{verdict}')
    return message


def check_tokens() -> bool:
    """Проверяет доступность переменных окружения."""
    return all((PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID))


def main():
    """Основная логика работы бота."""
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    if check_tokens() is False:
        message = 'Переменные окружения отсутствуют'
        logger.critical(message)
        raise ValueError(message)
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            if homeworks and len(homeworks):
                for homework in homeworks:
                    message = parse_status(homework)
                    send_message(bot, message)
            else:
                logger.debug('Новые статусы отсутствуют')
            current_timestamp = response['current_date']
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.critical(message)
            send_message(bot, message)
        else:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    logging.basicConfig(
        filename='main.log',
        format='%(asctime)s [%(levelname)s] %(message)s'
    )
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(handler)
    main()
