# Homework Bot

<img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/django/django-plain-wordmark.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/vscode/vscode-original-wordmark.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;

Homework Bot in Telegram, which connects to the external API of the Yandex Service and notifies the student with one of the statuses:

* the homework has been sent for review.

* the homework has been returned for correction.

* the homework has been accepted!

<img width="414" alt="homework" src="https://user-images.githubusercontent.com/96816183/182928201-5f94a1b3-4ee1-4172-a203-7fe64e202beb.png">

## **Getting Started:**

Clone the repository:

>*git clone git@github.com:airatns/homework_bot.git*

Set up the virtual environment:

>*python -m venv env* \
>*source env/scripts/activate*

Install dependencies in the app using requirements.txt:

>*python -m pip install --upgrade pip* \
>*pip install -r requirements.txt*

Create an .env file and fill it with the next data:

> PRACTICUM_TOKEN \
> TELEGRAM_TOKEN \
> TELEGRAM_CHAT_ID

Run the app locally:

>*python homework.py*
