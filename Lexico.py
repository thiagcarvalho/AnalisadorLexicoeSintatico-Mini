import TabelaHash
import Token
from Token import Words
from TabelaHash import Env


class Lexico:

    def __init__(self):
        self.Env = TabelaHash.Env()
        self.reserve(Words.If)
        self.reserve(Words.Else)
        self.reserve(Words.Prog)
        #self.reserve(Word.Beg)
        self.reserve(Words.End)
        self.reserve(Words.While)
        self.reserve(Words.Do)
        self.reserve(Words.Then)
        self.reserve(Words.For)
        self.reserve(Words.And)
        self.reserve(Words.Or)
        self.reserve(Words.Mod)
        self.reserve(Words.Int)
        self.reserve(Words.Dec)
        self.reserve(Words.Decl)
        self.reserve(Words.true)
        self.reserve(Words.false)
        self.reserve(Words.Read)
        self.reserve(Words.Write)

        self.Env.print()

    def reserve(self, Word):

        teste = [Word.lexeme, Word.tag]

        self.Env.put(Word.lexeme, teste)


lexico = Lexico()
