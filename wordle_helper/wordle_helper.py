from enum import Enum
from dataclasses import dataclass


class Color(Enum):
    GRAY = 0
    YELLOW = 1
    GREEN = 2

COLOR_PARSE_MAP = {
    "C": Color.GRAY,
    "Y": Color.YELLOW,
    "G": Color.GREEN
}

COLOR_PRINT_MAP = {
    Color.GRAY: "C",
    Color.YELLOW: "Y",
    Color.GREEN: "G"
}

@dataclass
class Letter:
    char: str
    color: Color
    def __str__(self):
        return f"{self.letter}[{self.color.name}]"

@dataclass
class Guess:
    letters: list[Letter]
    def __str__(self):
        return f"{''.join([l.char for l in self.letters])}[{''.join(COLOR_PRINT_MAP[l.color] for l in self.letters)}]"

class WordleWord:

    def __init__(self) -> None:
        self.allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.word = [set(self.allowed_chars) for _ in range(5)]
        self.required_chars = set({})

    def update(self, guess: Guess) -> None:
        for idx, letter in enumerate(guess.letters):

            if letter.color == Color.GRAY:
                for allowed in self.word:
                    if len(allowed) != 1:
                        allowed.discard(letter.char)

            elif letter.color == Color.YELLOW:
                self.word[idx].discard(letter.char)
                self.required_chars.add(letter.char)
            
            elif letter.color == Color.GREEN:
                self.word[idx] = set({letter.char})
                self.required_chars.add(letter.char)

class WordleFilter:

    def __init__(self) -> None:
        self._print_width = 10
        self.word_list = sorted(set([word.upper() for word in open("data/wordle_words.txt", "r").read().splitlines()]))
    
    def _has_required_chars(self, word: str, wordle_word: WordleWord) -> bool:
        rc = all(letter in word for letter in wordle_word.required_chars)
        return rc
    
    def _has_valid_chars(self, word: str, wordle_word: WordleWord) -> bool:
        vc = all(letter in wordle_word.word[idx] for idx, letter in enumerate(word))
        return vc

    def update(self, worlde_word: WordleWord) -> None:
        new_word_list = [word for word in self.word_list if self._has_required_chars(word, worlde_word) and self._has_valid_chars(word, worlde_word)]
        self.word_list = new_word_list

class Game:
    def __init__(self) -> None:
        self.start_words = sorted([word.upper() for word in open("data/start_words.txt", "r").read().splitlines()])
        self.ww = WordleWord()
        self.wf = WordleFilter()
    
    def reset(self) -> None:
        self.ww = WordleWord()
        self.wf = WordleFilter()
        self.run()
    
    def _print_columns(self, words: list[str], n: int) -> None:
        """ Pretty Prints spaced column of words of width `n` """
        print("\n".join(row for row in (" ".join([word for word in words[i:i+n]]) for i in range(0, len(words), n))))

    def _print_logo(self) -> None:
        """ Prints Wordle Helper logo to console """
        print("-"*68+"\n", end="")
        print("\n".join(line for line in open("data/logo.txt", "r").read().splitlines()))
        print("\n"+"-"*68+"\n")

    def parse_guess(self, guess: str) -> Guess:
        """ Parses a guess from the command line 
        Guesses should look like:
        "I:C R:Y A:G T:C E:Y"

        <LETTER>:<COLOR> (where C == charcoal, G == green, and Y == yellow)
        """
        letters = []
        for l in guess.upper().split():
            letter, color_str = l.split(":")
            letters.append(Letter(letter, COLOR_PARSE_MAP[color_str]))
        return Guess(letters)

    def run(self) -> None:
        self._print_logo()
        print("Best Starting Words:\n"+"-"*20)
        self._print_columns(self.start_words, 5)

        # Start game loop
        while True:
            print()
            guess_string = input("Enter Guess (<LETTER>:<COLOR>): ")
            if guess_string == "ng":
                self.reset()
            guess = self.parse_guess(guess_string)
            self.ww.update(guess)
            self.wf.update(self.ww)
            print("Valid Words:\n"+"-"*12)
            self._print_columns(self.wf.word_list, 10)
            print()


game = Game()
game.run()