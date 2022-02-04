FROM python:3

ADD wordle-telegram-bot.py /

COPY ./ /

RUN pip install -r requirements.txt

CMD ["python", "./wordle-telegram-bot.py"]