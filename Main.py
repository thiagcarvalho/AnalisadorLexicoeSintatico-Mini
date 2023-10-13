from Lexico import *
from Token import Token


def testeLexico(string):

    arq = string
    L = Lexico(arq)
    token = Token()

    token.setTag(L.getToken().getTag())

    while token.getTag() != Tag.FIM:

        print(f'TAG: {token.getTag()} LEXEMA: {token}')

        token.setTag(L.getToken().getTag())
        #print(token.getTag())
        #token.setTag(a_token.getTag())
        #print(token.getTag())



    print('Saiu')



arq = "teste.txt"  # Substitua pelo caminho do seu arquivo de texto

testeLexico(arq)




