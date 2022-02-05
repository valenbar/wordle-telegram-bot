# Wordle Telegram Bot
A unofficial Wordle game that you can play in Telegram.
Heavily inspired by: https://www.powerlanguage.co.uk/wordle/

Try it out: [@TheWordleBot](https://www.t.me/TheWordleBot)

This is how it looks like:

![This is an image](https://github.com/valenbar/wordle-telegram-bot/blob/main/assets/sample-output.png?raw=true)

## Features
- Play as many games as you want
- Languages: English, German, Swedish

## Setup

- Configure [example.env](https://github.com/valenbar/wordle-telegram-bot/blob/main/example.env)
- run `pip install -r requirements.txt`
- run `python wordle-telegram-bot.py`

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
- [ ] Option to change board size
- [ ] Notify if guess is in the wrong language
- [ ] Count game wins/loses per user
- [ ] Add Feedback option
- [ ] Language change starts new game
