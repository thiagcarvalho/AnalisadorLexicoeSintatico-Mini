from Lexico import *
from Token import Token
from Sintatico import *
import os

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


def testeSintatico(entrada, saida):

    arq = entrada
    arq_saida = saida
    S = Sintatico(arq, arq_saida)
    S.IniciaAnalise()

    print('\nImprimindo a Tabela de Simbolos')

    for key, value in S.Lex.Env.table.items():
        id = value[1]

        if len(value) > 2:
            tipo = value[2]
            print(f'ID: {key} \t Tipo: {tipo}')
        else:
            print(f'Lexema: {key} Tag: {id}')



arq = "testes_corrigidos/teste1.txt"  # Substitua pelo caminho do seu arquivo de texto

arq_saida = os.path.basename(arq)
arq_saida, extensao = arq_saida.split(".")
arq_saida = f"{arq_saida}_codigo"

#testeLexico(arq)
testeSintatico(arq, arq_saida)





