#! python

import enum
import json
import random

from ImageExport import ImageExport, WordleColors

class Outcome(enum.Enum):
    FINISHED = 1
    PROGRESS = 2
    WRONG = 3

class GameState(enum.Enum):
    INIT = 1
    PLAYING = 2
    WON = 3
    LOST = 4

class Wordle():

    wordle_dict = { "words_3": [], "words_4": [], "words_5": [], "words_6": [], "words_7": [] }
    wordle_dict_small = { "words_3": [], "words_4": [], "words_5": [], "words_6": [], "words_7": [] }
    board_x: int
    board_y: int
    target_word: str
    guessed_words: list()
    c_matrix = [[WordleColors]]
    state = GameState.INIT
    export: ImageExport


    def __init__(self, language: str):
        with open(f"./res/wordle_dict_{language}.json", "r") as f:
            self.wordle_dict = json.load(f)
        with open(f"./res/wordle_dict_10k_{language}.json", "r") as f:
            self.wordle_dict_small = json.load(f)


    def new_game(self, x: int, y: int):
        self.board_x = x
        self.board_y = y
        self.target_word = random.choice(self.wordle_dict_small[f"words_{x}"])
        self.guessed_words = []
        self.state = GameState.PLAYING
        self.c_matrix = [[WordleColors.gray for i in range(x)] for j in range(y)]
        self.export = ImageExport(self.board_x, self.board_y)
        self.current_img = self.export.get_image(self.c_matrix, self.guessed_words)
        return self.current_img


    def try_word(self, word: str):
        word = word.upper()
        if self.state == GameState.LOST or self.state == GameState.WON:
            return None
        result = self.check_rules(word)
        if result == Outcome.FINISHED or result == Outcome.PROGRESS:
            if len(self.guessed_words) < self.board_y:
                self.guessed_words.append(word)
                self.colorize_board()
            if result == Outcome.PROGRESS and len(self.guessed_words) == self.board_y:
                self.state = GameState.LOST
            self.current_img = self.export.get_image(self.c_matrix, self.guessed_words)
            return self.current_img
        else:
            self.state == GameState.PLAYING
        return None


    def check_rules(self, word: str) -> (Outcome):
        if word == "":
            return Outcome.WRONG
        elif word == self.target_word:
            self.state = GameState.WON
            return Outcome.FINISHED
        elif word in self.guessed_words:
            return Outcome.WRONG
        elif len(word) != self.board_x:
            return Outcome.WRONG
        elif word in self.wordle_dict[f"words_{self.board_x}"]:
            return Outcome.PROGRESS
        elif word not in self.wordle_dict[f"words_{self.board_x}"]:
            return Outcome.WRONG
        else:
            return Outcome.WRONG


    def colorize_board(self):
        for i, word in enumerate(self.guessed_words):
            green = {letter: 0 for letter in self.target_word}
            for j, char in enumerate(word):
                if char == self.target_word[j]:
                    self.c_matrix[i][j] = WordleColors.green
                    green[char] += 1
                elif char in self.target_word:
                    if green[char] < self.target_word.count(char):
                        self.c_matrix[i][j] = WordleColors.yellow
                    else:
                        self.c_matrix[i][j] = WordleColors.gray
                else:
                    self.c_matrix[i][j] = WordleColors.gray
