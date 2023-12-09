from Lexico import *
from Token import Token
from Sintatico import *

def testeLexico(string):

    arq = string
    L = Lexico(arq)
    token = L.getToken()

    #token.setTag(.getTag())

    partoken = Word(token.toString(), token.getTag())

    while partoken.getTag() != Tag.FIM:

        if partoken.getTag() == Tag.ID:
            print(f'ID: {partoken.toString()}')
        elif partoken.getTag() == Tag.LIT:
            print(f'Literal: {partoken.toString()}')
        elif partoken.getTag() == Tag.NUM:
            print(f'NUM: {partoken.toString()}')
        else:
            print(f'TAG: {partoken.getTag()} LEXEMA: {partoken.toString()}')

        token = L.getToken()
        partoken = Word(token.toString(), token.getTag())

    print('\nImprimindo a Tabela de Simbolos')

    for key, value in L.Env.table.items():
        id = value[1]

        if id == Tag.ID:
            print(f'ID: {key}')
        else:
            print(f'{key} Tag: {id}')


def testeSintatico(string):

    arq = string
    S = Sintatico(arq)

    if S.IniciaAnalise():
        print("Analise Sintatica feita com sucesso!")
    else:
        print("Falha na analisa sintática!")


arq = "testes_corrigidos/teste1.txt"  # Substitua pelo caminho do seu arquivo de texto

#testeLexico(arq)
testeSintatico(arq)





