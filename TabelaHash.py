from Token import *

class Env:
    def __init__(self):
        self.table = {}

    def put(self, tk, id, tipo = None):

        if tipo is None:
            self.table[tk] = id
        else:
            id.append(tipo)
            self.table[tk] = id
            print(self.table[tk])

    def get(self, tk):

        if tk in self.table:
            word = self.table[tk]
            #print(f'lexema é {word[0]} {word[1]} {word}')

            if len(word) > 2:
                return Word(word[0], word[1], word[2])
            return Word(word[0], word[1])

        return None

    def settype(self, tk, tipo):

        if tk in self.table:

            word = self.table[tk]
            word = Word(word[0], word[1])
            word.type(tipo)

            entrada = [word.lexeme, word.tag, word.tipo]

            self.put(word.lexeme, entrada)
            return Word(entrada[0], entrada[1], entrada[2])


    def print(self):
        print(self.table)
