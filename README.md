# Wordle Telegram Bot
A unofficial Wordle game that you can play in Telegram.
Heavily inspired by: https://www.powerlanguage.co.uk/wordle/

Try it out: [@TheWordleBot](https://www.t.me/TheWordleBot)

This is how it looks like:

![example_3.png](https://github.com/valenbar/wordle-telegram-bot/blob/main/assets/example_3.png?raw=true) | ![example_2.png](https://github.com/valenbar/wordle-telegram-bot/blob/main/assets/example_2.png?raw=true)
:----|----:
![example_1.png](https://github.com/valenbar/wordle-telegram-bot/blob/main/assets/example_1.png?raw=true) | ![example_4.png](https://github.com/valenbar/wordle-telegram-bot/blob/main/assets/example_4.png?raw=true)

## Features
- Play as many games as you want
- Languages: English, German, Swedish

## Setup

Clone repository:

    git clone https://github.com/valenbar/wordle-telegram-bot

Configure [example.env](https://github.com/valenbar/wordle-telegram-bot/blob/main/example.env)

    cd wordle-telegram-bot

#### Without Docker

Install python requirements

    pip install -r requirements.txt

Start the program

    python wordle-telegram-bot.py

#### With Docker

```bash
docker build -t wordle_telegram_bot .
docker volume create wordle_data
docker run -d -v wordle_data:/app --name wordle_app wordle_telegram_bot
```

## TODO

- [x] Feature to change language
- [x] Simpler word pool
- [x] Delete user message when when word is not added to board
- [x] Update unique users count to log channel
- [x] Remove yellow letter if that letter is already green and there is no other
- [x] Add more markdown to log channel messages
- [x] Save all word guesses to a dictionary to find most common guesses
- [x] Add resources.txt
- [x] Add Hard-mode
- [x] Option to change board size
- [x] Add Feedback option
- [ ] Notify if guess is in the wrong language
- [ ] Count game wins/loses per user
- [ ] Option to report a bad word after the game
- [ ] Sync guessed words dictionary to google spreadsheet
- [ ] Option to get a hint on the last guess, e.g. an example sentence or the definition
