FROM python:3.11

WORKDIR /wordle

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "./wordle-telegram-bot.py"]
