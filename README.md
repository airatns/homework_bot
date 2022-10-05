# Homework Bot

Telegram-бот, который обращается к API сервиса Практикум.Домашка и оповещает студента Практикума одним из статусов:

* Работа взята на проверку ревьюером.

* Работа проверена: у ревьюера есть замечания.

* Работа проверена: ревьюеру всё понравилось. Ура!

<img width="414" alt="homework" src="https://user-images.githubusercontent.com/96816183/182928201-5f94a1b3-4ee1-4172-a203-7fe64e202beb.png">

## **Стек технологий**

Python, Django, Telegram Bot

## **Как запустить проект:**

Клонировать репозиторий и перейти в него в командной строке:

>*git clone git@github.com:airatns/homework_bot.git*

Cоздать и активировать виртуальное окружение:

>*python -m venv env* \
>*source env/scripts/activate*

Установить зависимости из файла requirements.txt:

>*python -m pip install --upgrade pip* \
>*pip install -r requirements.txt*

Прописать параметры окружения в файле .env:

>* PRACTICUM_TOKEN \
>* TELEGRAM_TOKEN \
>* TELEGRAM_CHAT_ID

Запустить проект:

>*python homework.py*
