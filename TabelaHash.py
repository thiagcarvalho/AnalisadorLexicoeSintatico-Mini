from Token import *


class Env:
    def __init__(self):
        self.table = {}

    def put(self, tk, id):
        self.table[tk] = id

    def get(self, tk):
        if tk in self.table:
            word = self.table[tk]
            return Word(word.lexeme, word.getTag())
        return None

    def print(self):
        print(self.table)
