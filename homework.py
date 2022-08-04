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
    except Exception:
        message = 'Произошел сбой при отправке сообщения'
        logger.error(message)


def get_api_answer(current_timestamp):
    """Получает временную метку.
    Делает запрос к единственному эндпоинту API-сервиса
    и возвращает ответ API.
    """
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        response = requests.get(url=ENDPOINT, headers=HEADERS, params=params)
    except Exception:
        message = 'Наблюдаются сбои при запросе к эндпоинту'
        logger.error(message)
        raise ValueError(message)
    if response.status_code == 200:
        return response.json()
    else:
        message = 'Эндпоинт недоступен'
        logger.error(message)
        raise ValueError(message)


def check_response(response):
    """Получает ответ API.
    Возвращает список домашних работ из ответа API.
    """
    homeworks_list = response['homeworks']
    if not isinstance(response, dict):
        message = 'Ответ API представлен не в виде словаря'
        logger.error(message)
        raise ValueError(message)
    if not bool(response):
        message = 'Ответ API пришел в виде пустого словаря'
        logger.error(message)
        raise ValueError(message)
    if not isinstance(homeworks_list, list):
        message = 'Домашние задания представлены не в виде списка'
        logger.error(message)
        raise ValueError(message)
    if 'homeworks' not in response:
        return False
    return homeworks_list


def parse_status(homework):
    """Получает один элемент из списка домашних работ.
    Возвращает статус этой работы.
    """
    homework_name = homework['homework_name']
    homework_status = homework['status']
    try:
        all((homework_name, homework_status))
        if homework_status in HOMEWORK_VERDICTS:
            verdict = HOMEWORK_VERDICTS[homework_status]
            message = (f'Изменился статус проверки работы "{homework_name}". '
                       f'{verdict}')
            return message
        message = f'Статус {homework_status} недокументирован'
        logger.error(message)
        raise ValueError(message)
    except Exception:
        message = 'Ключи "homework_name" и "status" в списке отсутствуют'
        logger.error(message)
        raise ValueError(message)


def check_tokens() -> bool:
    """Проверяет доступность переменных окружения."""
    return all((PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID))


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        message = 'Переменные окружения отсутствуют'
        logger.critical(message)
        raise ValueError(message)
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    send_message(bot, 'Бот запущен')
    current_timestamp = int(time.time())
    initial_message = ''
    while True:
        try:
            response = get_api_answer(current_timestamp)
            current_timestamp = response['current_date']
            homework = check_response(response)
            if homework:
                current_homework = homework[0]
                message = parse_status(current_homework)
                send_message(bot, message)
            else:
                message = 'В списке отсутствуют новые статусы'
                logger.error(message)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(message)
            if message != initial_message:
                initial_message = message
                send_message(bot, message)
        finally:
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
