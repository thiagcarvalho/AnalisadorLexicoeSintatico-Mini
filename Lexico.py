import TabelaHash
from Token import Token, Num
from Tag import Tag
from Token import Words, Word
from TabelaHash import Env
import re


terminais = {"program", "declare", "begin", "end", "integer", "decimal", "if", "then", "else",
                     "do", "while", "for", "to", "read", "write", "not", "or", "mod", "and", "=", "+",
                     "-", "*", "/", "<", ">", "<=", ">=", "<>", "<<", ">>", "<<<", ">>>", ":=", ";", ",", "\"",
                     "?", ":", ".", "(", ")"}

letters = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
                   'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                   'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                   'z'}


digits= {'0','1', '2', '3', '4', '5', '6', '7', '8', '9'};

class Lexico:

    def __init__(self, arq):
        self.Env = TabelaHash.Env()
        self.arq = arq
        self.pos = 0
        self.char = ''

        self.reserve(Words.If)
        self.reserve(Words.Else)
        self.reserve(Words.Prog)
        self.reserve(Words.Beg)
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
        #self.reserve(Words.Atrib)
        self.reserve(Words.Int)
        #self.reserve(Words.Com)
        #self.reserve(Words.Smc)

    def getToken(self):

        try:
            with open(self.arq, 'r') as arquivo:

                arquivo.seek(self.pos)

                char = arquivo.read(1)

                #print(f'Lendo o caractere {char}')
                #Lê espaços vazios e qubra de linha

                while char.isspace() or char == '\n' or char == '%':

                    if char == '%':
                        arquivo.readline()
                    """while char != '\n':
                        char = arquivo.read(1)
                        #print(char)"""


                    char = arquivo.read(1)

                if not char:
                    # print('Fim do arquivo')

                    fim = Word('FIM', Tag.FIM)
                    return fim

                if char == ">":
                    char = arquivo.read(1)

                    if char == ">":

                        char = arquivo.read(1)
                        self.pos = arquivo.tell()

                        if char == ">":
                            return Words.Ggg

                        return Words.Gg

                    elif char == "=":
                        self.pos = arquivo.tell()
                        return Words.Ge

                    self.pos = arquivo.tell() - 1
                    return Words.Gt

                if char == "<":

                    char = arquivo.read(1)

                    if char == "=":
                        self.pos = arquivo.tell()
                        return Words.Le
                    elif char == ">":
                        self.pos = arquivo.tell()
                        return Words.Ne

                    elif char == "<":
                        char = arquivo.read(1)
                        self.pos = arquivo.tell()

                        if char == "<":
                            return Words.Lll

                        return Words.Ll

                    self.pos = arquivo.tell()
                    return Words.Lt

                if char == "=":
                    self.pos = arquivo.tell()
                    return Words.Eq

                if char == ":":
                    char = arquivo.read(1)
                    if char == "=":
                        self.pos = arquivo.tell()

                        return Words.Atrib

                    self.pos = arquivo.tell() - 1
                    return Words.Clm

                if char == ",":
                    self.pos = arquivo.tell()
                    return Words.Com

                if char == ";":
                    self.pos = arquivo.tell()
                    return Words.Smc

                if char == "(":
                    self.pos = arquivo.tell()
                    return Words.Opar

                if char == ")":
                    self.pos = arquivo.tell()
                    return Words.Cpar

                if char == "*":
                    self.pos = arquivo.tell()
                    return Words.Mlt

                if char == "?":
                    self.pos = arquivo.tell()
                    return Words.Qst

                if char == "/":
                    self.pos = arquivo.tell()
                    return Words.Div

                if char == "-":
                    self.pos = arquivo.tell()
                    return Words.Sub

                if char == "+":
                    self.pos = arquivo.tell()
                    return Words.Add

                if char == "?":
                    self.pos = arquivo.tell()
                    return Words.Qst


                if char == '"':
                    literal = char
                    char = arquivo.read(1)

                    while char != '"':
                        literal += char
                        char = arquivo.read(1)

                    self.pos = arquivo.tell()

                    literal += char
                    teste = Word(literal, Tag.LIT)

                    return teste

                if self.eDigito(char):
                    numero = 0

                    while self.eDigito(char):
                        numero = 10*numero + int(char)
                        char = arquivo.read(1)

                    #digit = Num(numero)
                    numero = Word(str(numero), Tag.NUM)
                    self.pos = arquivo.tell() - 1

                    return numero

                if self.eLetra(char):
                    palava = ""

                    while self.eLetra(char) or self.eDigito(char):

                        palava += char
                        char = arquivo.read(1)
                        #print(char)

                    #print(f'Li "{palava}" e estou nesse caractere {char}')
                    if char != "":
                        self.pos = arquivo.tell() - 1
                    else:
                        self.pos = arquivo.tell()

                    teste = self.Env.get(palava)

                    if teste:
                        return teste

                    teste = Word(palava, Tag.ID)
                    self.reserve(teste)
                    return teste
                    #print(teste.lexeme, teste.getTag())

                self.pos = arquivo.tell()
                print(f"Erro léxico: O token não foi reconhecido: {char}")
                Token = Word(char, -1)
                return Token


        except FileNotFoundError:
            print(f"O arquivo '{self.arq}' não foi encontrado.")

    def reserve(self, Word):
        teste = [Word.lexeme, Word.tag]


        self.Env.put(Word.lexeme, teste)

    def eLetra(self, char):
        if len(char) == 1:
            return char.isalpha()
        return False

    def eNumero(self, char):
        if len(char) == 1:
            return char.isdigit()
        return False

    def eDigito(self, char):
        if len(char) == 1:
            return char.isdigit()
        return False