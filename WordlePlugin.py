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
    board_x: int
    board_y: int
    target_word: int
    guessed_words: list()
    c_matrix = [[WordleColors]]
    state = GameState.INIT
    export: ImageExport


    def __init__(self):
        # super(Wordle, self).__init__(*args)
        # self.board_x = x
        # self.board_y = y
        with open('./res/wordle_dict.json', 'r') as f:
            self.wordle_dict = json.load(f)


    def new_game(self, x: int, y: int, lan: str):
        self.board_x = x
        self.board_y = y
        self.target_word = random.choice(self.wordle_dict["words_" + str(x)])
        self.guessed_words = []
        self.state = GameState.PLAYING
        self.c_matrix = [[WordleColors.gray for i in range(x)] for j in range(y)]
        self.export = ImageExport(self.board_x, self.board_y)

        return self.export.get_image(self.c_matrix, self.guessed_words)


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
            print("state:", self.state)
            return self.export.get_image(self.c_matrix, self.guessed_words)
        else:
            self.state == GameState.PLAYING
        return None


    def check_rules(self, word: str) -> (Outcome):
        if word == "":
            print("You didn't enter anything!")
            return Outcome.WRONG
        elif word == self.target_word:
            print("Correct!")
            self.state = GameState.WON
            return Outcome.FINISHED
        elif word in self.guessed_words:
            print("You already guessed that!")
            return Outcome.WRONG
        elif len(word) != self.board_x:
            print("Word lenght is not correct")
            return Outcome.WRONG
        elif word in self.wordle_dict[f"words_{self.board_x}"]:
            print("Not the right word")
            return Outcome.PROGRESS
        elif word not in self.wordle_dict[f"words_{self.board_x}"]:
            print("Word not in dictionary")
            return Outcome.WRONG
        else:
            print("Something went wrong")
            return Outcome.WRONG


    def colorize_board(self):
        for i, word in enumerate(self.guessed_words):
            for j, char in enumerate(word):
                if char == self.target_word[j]:
                    self.c_matrix[i][j] = WordleColors.green
                elif char in self.target_word:
                    self.c_matrix[i][j] = WordleColors.yellow
                else:
                    self.c_matrix[i][j] = WordleColors.gray