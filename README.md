# Homework Bot

Telegram-бот, который обращается к API сервиса Практикум.Домашка и оповещает студента Практикума одним из статусов:

* работа принята на проверку

* работа возвращена для исправления замечаний

* работа принята

## **Стек технологий**

Python, Django, Telegram Bot

## **Как запустить проект:**

Клонировать репозиторий и перейти в него в командной строке:

>*git clone git@github.com:airatns/homework_bot.git*

Cоздать и активировать виртуальное окружение:

>*python3 -m venv env*

>*source env/scripts/activate*

Установить зависимости из файла requirements.txt:

>*python3 -m pip install --upgrade pip*

>*pip install -r requirements.txt*

Выполнить миграции:

>*python3 manage.py migrate*

Прописать параметры окружения в файле .env:

>* PRACTICUM_TOKEN

>* TELEGRAM_TOKEN

>* TELEGRAM_CHAT_ID

Запустить проект:

>*python3 manage.py runserver*


