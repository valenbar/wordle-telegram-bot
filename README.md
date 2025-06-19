# Wordle Telegram Bot
A unofficial Wordle game that you can play in Telegram.
Heavily inspired by: https://www.powerlanguage.co.uk/wordle/

Try it out: [@TheWordleBot](https://www.t.me/TheWordleBot)

This is how it looks like:

![example_3.png](https://github.com/valenbar/wordle-telegram-bot/blob/main/assets/example_3.png?raw=true) | ![example_2.png](https://github.com/valenbar/wordle-telegram-bot/blob/main/assets/example_2.png?raw=true) | ![example_1.png](https://github.com/valenbar/wordle-telegram-bot/blob/main/assets/example_1.png?raw=true) | ![example_4.png](https://github.com/valenbar/wordle-telegram-bot/blob/main/assets/example_4.png?raw=true)
:----|----|----|----:

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

##### Docker Compose

```yaml
services:
  wordle:
    container_name: wordle-telegram-bot
    build: 
      context: https://github.com/valenbar/wordle-telegram-bot.git
      dockerfile: Dockerfile
    volumes:
      # where to store persistent data
      - </path/to/data>:/wordle/data
    # env_file: .env
    environment:
      # The token you get from botfather
      API_TOKEN: "" 
      # The channel id of the telegram channel that you want to use for logging
      # leave empty if you don't want to use that
      LOG_CHANNEL: ""
```

##### Docker Run
```bash
docker build -t wordle-telegram-bot .

docker run -d \
  -v </path/to/data>:/wordle/data \
  --name wordle-telegram-bot \
  -e API_TOKEN="" \
  -e LOG_CHANNEL="" \
  wordle-telegram-bot
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
- [x] Option to get a hint, e.g. an example sentence or the definition
- [ ] Notify if guess is in the wrong language
- [ ] Count game wins/loses per user
- [ ] Option to report a bad word after the game
- [ ] Sync guessed words dictionary to google spreadsheet
- [ ] Error handling when pickled data is corrupted
