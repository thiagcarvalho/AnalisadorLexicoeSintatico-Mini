import TabelaHash
from Token import Token, Num
from Tag import Tag
from Token import Words
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

    def getToken(self):

        try:
            with open(self.arq, 'r') as arquivo:

                arquivo.seek(self.pos)
                char = arquivo.read(1)

                while char == ' ' or char == '\n':
                    if char == '\n':
                        arquivo.readline()

                    char = arquivo.read(1)

                if char == '':
                    #print('Fim do arquivo')
                    fim = Token()
                    fim.setTag(Tag.FIM)

                    return fim


                if self.eDigito(char):
                    numero = 0

                    while self.eDigito(char):
                        numero = 10*numero + int(char)
                        char = arquivo.read(1)

                    digit = Num(numero)
                    self.pos = arquivo.tell()

                    return digit

                if self.eLetra(char):
                    palava = ""

                    while self.eLetra(char) or self.eDigito(char):

                        palava += char
                        char = arquivo.read(1)

                    teste = self.Env.get(palava)
                    self.pos = arquivo.tell()

                    return teste
                    #print(teste.lexeme, teste.getTag())

                """while True:
                    # Lê um único caractere do arquivo
                    caractere = arquivo.read(1)
                    # Verifica se o fim do arquivo foi atingido

                    #if not caractere:
                        #print("Trem em branco")
                        #break

                    if caractere.isspace():
                        # Se encontramos um espaço em branco, o token está completo

                        #self.pos = arquivo.tell()

                        print(f'Caractere: {token} e posição {self.pos}')

                        #self.arq = arquivo.seek(arquivo.tell())
                        break

                        # Adiciona o caractere ao token
                    token += caractere
                    print(token)
                    # Faça algo com o caractere"""


                # Faça algo com o conteúdo do arquivo
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