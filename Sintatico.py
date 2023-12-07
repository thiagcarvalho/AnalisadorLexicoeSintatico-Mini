from Lexico import *

class Sintatico:

    def __init__(self, arq):

        self.Lex = Lexico(arq)
        self.pilha_token = []

    def nextToken(self):

        if not self.pilha_token:
            token = self.Lex.getToken()
            print(f'Recebido o token: {token.toString()} do Léxico')

            return token

        else:
            token = self.pilha_token[-1]
            self.pilha_token.pop()
            return token

    def AddToken(self, a):

        self.pilha_token.append(a)

    # S->*program id body $
    def IniciaAnalise(self):

        token = self.nextToken()
        b = True

        while token.getTag() != Tag.FIM:

            if token.getTag() == Tag.PRG:
                b = self.e1() and b
                break

            else:
                print(f'ERRO! Esperado a palavra "program", recebido {token.toString()}')

            token = self.nextToken()


        return b

    # S->program* id body $
    def e1(self):

        token = self.nextToken()
        b = True

        while token.getTag() != Tag.FIM:

            if token.getTag() == Tag.ID:
                b = self.e2() and b
                break

            else:
                print(f'ERRO! Esperado um "id", recebido {token.toString()}')

            token = self.nextToken()

        return b

    # S->program id* body $
    def e2(self):

        token = self.nextToken()
        b = True

        while token.getTag() != Tag.FIM:

            if token.getTag() == Tag.DECL:
                b = self.e3() and b

            elif token.getTag() == Tag.BGN:
                b = self.e10() and b

            elif token.getTag() == Tag.BODY:
                b = self.e33() and b
                return b

            else:
                b = False
                print(f'ERRO! Esperado a palavra "declare" ou "begin", recebido {token.toString()}')

            token = self.nextToken()

        return b

    #body -> declare * dec-lst begin stmt-lst end
    def e3(self):

        token = self.nextToken()
        b = True

        while token.getTag() != Tag.FIM:

            # body -> declare *dec-lst begin stmt-lst end
            if token.getTag() == Tag.DECLLST:
                b = self.e9() and b
                return b

            # type -> *integer
            elif token.getTag() == Tag.INT:
                aux = Word('Type',Tag.TYPE)
                self.AddToken(aux)

            # typer -> *decimal
            elif token.getTag() == Tag.DEC:
                aux = Word('Type', Tag.TYPE)
                self.AddToken(aux)

            #decl -> *type ident-lst
            elif token.getTag() == Tag.TYPE:
                #self.AddToken(token)
                b = self.e4() and b

            # decl-list -> *decl decl-list'
            elif token.getTag() == Tag.DECL:
                b = self.e7() and b

            else:
                b = False
                print(f'ERRO! Esperado "int", "decimal", recebido {token.toString()}')

            token = self.nextToken()

        return b

    #decl -> type * indent-list
    #indet-list -> * identifier indent-list'
    def e4(self):

        token = self.nextToken()

        b = True

        while token.getTag() != Tag.FIM:

            if token.getTag() == Tag.ID:

                self.AddToken(token)
                b = self.e5() and b

            elif token.getTag() == Tag.IDLST:

                aux = Word('Decl', Tag.DECL)
                self.AddToken(aux)

                return b

            else:
                b = False
                print(f'ERRO! Esperado "identificador", recebido {token.toString()}')

            token = self.nextToken()
            #print('estado 4')

        return b

    #ident-list -> identifier * indent-list'
    #ident-list' -> *, ident-list
    def e5(self):

        aux = self.nextToken()

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            if token.getTag() == Tag.COM:

                self.AddToken(token)
                b = self.e6() and b

            elif token.getTag() == Tag.IDLSTL:
                aux = Word('IDLST', Tag.IDLST)
                self.AddToken(aux)
                return b

            else:

                aux = Word('IDLSTL',Tag.IDLSTL)
                self.AddToken(token)
                self.AddToken(aux)

            token = self.nextToken()

        return b

    #ident-list' -> , *  ident-list
    #ident-list -> * id ident-list'
    def e6(self):

        aux = self.nextToken()

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            if token.getTag() == Tag.ID:

                self.AddToken(token)
                b = self.e5() and b

            elif token.getTag() == Tag.IDLST:

                aux = Word('IDLSTL', Tag.IDLSTL)
                self.AddToken(aux)

                return b

            else:
                b = False
                print(f'ERRO! Esperado "identificador", recebido {token.toString()}')

            token = self.nextToken()

        return b

    #decl-list -> decl *; [decl;]
    def e7(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            if token.getTag() == Tag.SMC:
                b = self.e8() and b
                return b

            else:
                b = False
                print(f'ERRO! Esperado ";" recebido {token.toString()}')

            token = self.nextToken()

        return b

    #decl-lst -> decl; * [decl;]
    def e8(self):

        b = True

        token = self.nextToken()


        while token.getTag() != Tag.FIM:

            if token.getTag() == Tag.INT:
                aux = Word('Type', Tag.TYPE)
                self.AddToken(aux)

            elif token.getTag() == Tag.DEC:
                aux = Word('Type', Tag.TYPE)
                self.AddToken(aux)

            elif token.getTag() == Tag.TYPE:

                #self.AddToken(token)
                b = self.e4() and b

            elif token.getTag() == Tag.DECL:
                b = self.e7() and b
                return b

            elif token.getTag() == Tag.BGN or token.getTag() == Tag.SMC:

                aux = Word('DECLLST', Tag.DECLLST)
                self.AddToken(token)
                self.AddToken(aux)

                return b

            else:
                b = False
                print(f'ERRO! Esperado "int", "decimal", recebido {token.toString()}')

            token = self.nextToken()
            #print('estado 8')

        return b

    #body -> declare decl-lst *begin stm-lst end
    def e9(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            if token.getTag() == Tag.BGN:
                b = self.e10() and b
                return b

            else:
                b = False
                print(f'ERRO! Esperado "begin", recebido: {token.toString()}')

            token = self.nextToken()

        return b

    #body -> begin *stmt-list end
    #body -> declare dec-lst begin *stmt-list end
    def e10(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            if token.getTag() == Tag.STMTLST:
                b = self.e32() and b
                return b

            #stmt-list -> *stmt; [stmt;]
            elif token.getTag() == Tag.STMT:
                b = self.e19() and b

            #stmt -> assign-stmt
            elif token.getTag() == Tag.ASSIGNSTMT:
                aux = Word('STMT', Tag.STMT)
                self.AddToken(aux)

            elif token.getTag() == Tag.DOWHILESTMT:
                aux = Word('STMT', Tag.STMT)
                #aux = Token(Tag.STMT)
                self.AddToken(aux)

            # stmt -> *readstmt
            elif token.getTag() == Tag.READSTMT:
                aux = Word('STMT', Tag.STMT)
                #aux = Token(Tag.STMT)
                self.AddToken(aux)

            # stmt -> if-stmt
            elif token.getTag() == Tag.IFSTMT:
                aux = Word('STMT', Tag.STMT)
                #aux = Token(Tag.STMT)
                self.AddToken(aux)

            # stmt => write-stmt
            elif token.getTag() == Tag.WRITESTMT:
                aux = Word('STMT', Tag.STMT)
                #aux = Token(Tag.STMT)
                self.AddToken(aux)

            # assign-stmt -> *identifier := simple_Expr
            elif token.getTag() == Tag.ID:
                b = self.e17() and b

            # if-stmt -> *if condition then stmt-list end
            # if-stmt -> *if condition then stmt-list else stm-list end
            elif token.getTag() == Tag.IF:
                b = self.e39() and b

            # do-while-stmt -> *do stmt-list stmt-suffix
            elif token.getTag() == Tag.DO:
                b = self.e35() and b

            #read-stmt -> *read(identifier)
            elif token.getTag() == Tag.READ:
                b = self.e11() and b

            #write-stmt -> *write(writable)
            elif token.getTag() == Tag.WRITE:
                b = self.e12() and b

            else:
                b = False
                print(f'ERRO! Esperado "identifier", "if", "while", "read" ou "write", recebido: {token.toString()}')

            token = self.nextToken()

        return  b

    # read-stmt -> read*(identifier)
    def e11(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            if token.getTag() == Tag.OPAR:
                b = self.e15() and b
                return b
            else:
                b = False
                print(f'ERRO! Esperado "(", recebido: {token.toString()}')

            token = self.nextToken()


        return b

    # write-stmt -> write*(writable)
    def e12(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            if token.getTag() == Tag.OPAR:
                b = self.e13() and b
                return b
            else:
                b = False
                print(f'ERRO! Esperado "(", recebido: {token.toString()}')

            token = self.nextToken()


        return b

    # write-stmt -> write(*writable)
    def e13(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            #write-stmt -> write(*writable)
            if token.getTag() == Tag.WRITEABLE:
                b = self.e14() and b
                return b

            #writable -> simple_Expr
            #simple_Expr -> simple_Expr addop term
            elif token.getTag() == Tag.SIMPLEEXPRESSION:
                b = self.e34() and b

            #writable -> literal
            elif token.getTag() == Tag.LIT:
                aux = Word('WRITEABLE', Tag.WRITEABLE)
                #aux = Token(Tag.WRITEABLE)
                self.AddToken(aux)

            # simple_Expr -> *term
            # term -> *term mulop factor_a
            elif token.getTag() == Tag.TERM:
                b = self.e22() and b

            # term -> *factor_a
            elif token.getTag() == Tag.FACTORA:
                aux = Word('TERM', Tag.TERM)
                #aux = Token(Tag.TERM)
                self.AddToken(aux)

            # factor_a -> *factor
            elif token.getTag() == Tag.FACTOR:
                aux = Word('FACTOR-A', Tag.FACTORA)
                #aux = Token(Tag.FACTORA)
                self.AddToken(aux)

            # factor_a -> *not factor
            elif token.getTag() == Tag.NOT:
                b = self.e21() and b

            # factor_a -> *- factor
            elif token.getTag() == Tag.SUB:
                b = self.e31() and b

            elif token.getTag() == Tag.ID:
                aux = Word('FACTOR', Tag.FACTOR)
                #aux = Token(Tag.FACTOR)
                self.AddToken(aux)

            # factor -> *constant
            elif token.getTag() == Tag.NUM:
                aux = Word('FACTOR', Tag.FACTOR)
                #aux = Token(Tag.FACTOR)
                self.AddToken(aux)

            # simple_Expr -> ? simple_Expr : simple_Expr
            # factor -> *(expression)
            elif token.getTag() == Tag.OPAR:
                b = self.e45() and b

            else:

                b = False
                print(f'ERRO! Esperado "LITERAL", "identificador", "numero", "(", "-" ou "not", recebido '
                      f'{token.toString()}')

            token = self.nextToken()

        return b

    # write-stmt -> write(writable*)
    def e14(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            if token.getTag() == Tag.CPAR:

                aux = Word('WRITESTMT', Tag.WRITESTMT)
                #aux = Token(Tag.WRITESTMT)
                self.AddToken(aux)
                return b

            else:
                b = False
                print(f'ERRO! Esperado ")", recebido: {token.toString()}')

            token = self.nextToken()

        return b


    # read-stmt -> read(*identifier)
    def e15(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            if token.getTag() == Tag.ID:
                b = self.e16() and b
                return b

            else:
                b = False
                print(f'ERRO! Esperado "identifier", recebido: {token.toString()}')

            token = self.nextToken()

        return b

    # read-stmt -> read(identifier*)
    def e16(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            if token.getTag() == Tag.CPAR:
                aux = Word('READSTMT', Tag.READSTMT)
                #aux = Token(Tag.READSTMT)
                self.AddToken(aux)
                return b
            else:
                b = False
                print(f'ERRO! Esperado ")", recebido: {token.toString()}')

            token = self.nextToken()

        return b

    #assign-stmt -> identifier* := simple_Expr
    def e17(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            if token.getTag() == Tag.ATRIB:
                b = self.e18() and b
                return b
            else:
                b = False
                print(f'ERRO! Esperado ":=" recebido, {token.toString()}')

            token = self.nextToken()

        return b

    #assign-stmt -> identifier :=* simple_Expr
    def e18(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            #assign-stmt -> identifier := *simple_Expr
            #simple_Exprt -> *simple_Exprt addop simple_Expr
            if token.getTag() == Tag.SIMPLEEXPRESSION:
                b = self.e38() and b
                return b

            # simple_Expr -> *term
            # term -> *term mulop factor_a
            elif token.getTag() == Tag.TERM:
                b = self.e22() and b

            # simple_Expr -> (*simple_Expr) ? simple_Expr : simple_Expr
            # factor -> *(expression)
            elif token.getTag() == Tag.OPAR:
                b = self.e45() and b


            #term -> *factor_a
            elif  token.getTag() == Tag.FACTORA:
                aux = Word('TERM', Tag.TERM)
                #aux = Token(Tag.TERM)
                self.AddToken(aux)

            #factor_a -> *factor
            elif token.getTag() == Tag.FACTOR:
                aux = Word('FACTOR-A', Tag.FACTORA)
                #aux = Token(Tag.FACTORA)
                self.AddToken(aux)

            # factor_a -> *not factor
            elif token.getTag() == Tag.NOT:
                b = self.e21() and b

            # factor_a -> *not factor
            elif token.getTag() == Tag.SUB:
                b = self.e31() and b

            elif token.getTag() == Tag.ID:
                aux = Word('FACTOR', Tag.FACTOR)
                #aux = Token(Tag.FACTOR)
                self.AddToken(aux)

            #factor -> *constant
            elif token.getTag() == Tag.NUM:
                aux = Word('FACTOR', Tag.FACTOR)
                #aux = Token(Tag.FACTOR)
                self.AddToken(aux)

            else:
                b = False
                print(f'ERRO! Esperado "(", "-", "not", "identificadoe" ou "numero", recebido {token.toString()}')

            token = self.nextToken()
            #print('estado 18')


        return  b

    # stmt-list -> stmt*; [stmt;]
    def e19(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            if token.getTag() == Tag.SMC:
                b = self.e20() and b
                return b

            else:
                b = False
                print(f'ERRO! Esperado ";" recebido {token.toString()}')

            token = self.nextToken()
            #print('estado 19')

        return b

    #stmt-list -> stmt;* [stmt;]
    def e20(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            # stmt-list -> stmt; stmt*;
            if token.getTag() == Tag.STMT:
                b = self.e19() and b
                return b

            # stmt -> *assign-stmt
            elif token.getTag() == Tag.ASSIGNSTMT:
                #print(f'o valor do b é {b}')
                aux = Word('STMT', Tag.STMT)
                #aux = Token(Tag.STMT)
                self.AddToken(aux)

            # stmt -> *readstmt
            elif token.getTag() == Tag.READSTMT:
                aux = Word('STMT', Tag.STMT)
                #aux = Token(Tag.STMT)
                self.AddToken(aux)

            # stmt -> if-stmt
            elif token.getTag() == Tag.IFSTMT:
                aux = Word('STMT', Tag.STMT)
                #aux = Token(Tag.STMT)
                self.AddToken(aux)

            # stmt -> *do-while-stmt
            elif token.getTag() == Tag.DOWHILESTMT:
                aux = Word('STMT', Tag.STMT)
                #aux = Token(Tag.STMT)
                self.AddToken(aux)

            # stmt => write-stmt
            elif token.getTag() == Tag.WRITESTMT:
                aux = Word('STMT', Tag.STMT)
                #aux = Token(Tag.STMT)
                self.AddToken(aux)

            # assign-stmt -> *identifier := simple_Expr
            elif token.getTag() == Tag.ID:
                b = self.e17() and b

            # if-stmt -> *if condition then stmt-list end
            # if-stmt -> *if condition then stmt-list else stm-list end
            elif token.getTag() == Tag.IF:
                b = self.e39() and b

            # do-while-stmt -> *do stmt-list stmt-suffix
            elif token.getTag() == Tag.DO:
                b = self.e35()

            # read-stmt -> *read(identifier)
            elif token.getTag() == Tag.READ:
                b = self.e11() and b

            # write-stmt -> *write(writable)
            elif token.getTag() == Tag.WRITE:
                b = self.e12() and b

            else:

                aux = Word('STMTLST', Tag.STMTLST)
                #aux = Token(Tag.STMTLST)
                self.AddToken(token)
                self.AddToken(aux)

                return b

            token = self.nextToken()

        return b

    # factor_a -> not *factor
    def e21(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:


            #factor_a -> not *factor
            if token.getTag() == Tag.FACTOR:
                aux = Word('FACTOR-A', Tag.FACTORA)
                #aux = Token(Tag.FACTORA)
                self.AddToken(aux)
                return b

            #factor -> *identifier
            elif token.getTag() == Tag.ID:
                aux = Word('FACTOR', Tag.FACTOR)
                #aux = Token(Tag.FACTOR)
                self.AddToken(aux)

            # factor -> *constant
            elif token.getTag() == Tag.NUM:
                aux = Word('FACTOR', Tag.FACTOR)
                #aux = Token(Tag.FACTOR)
                self.AddToken(aux)

            # factor -> *(expression)
            elif token.getTag() == Tag.OPAR:
                b = self.e21() and b

            else:
                b = False
                print(f'ERRO! Esperado "id", "numero" ou "(", recebido: {token.toString()}')

            token = self.nextToken()

        return b

    # simple_Expr -> term*
    # term -> term * mulop factor_a
    def e22(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            # term -> term mulop* factor_a
            if token.getTag() == Tag.MULOP:
                b = self.e23() and b
                return b

            elif token.getTag() == Tag.MLT:
                aux = Word('MULOP', Tag.MULOP)
                #aux = Token(Tag.MULOP)
                self.AddToken(aux)

            elif token.getTag() == Tag.DIV:
                aux = Word('MULOP', Tag.MULOP)
                #aux = Token(Tag.MULOP)
                self.AddToken(aux)

            elif token.getTag() == Tag.AND:
                aux = Word('MULOP', Tag.MULOP)
                #aux = Token(Tag.MULOP)
                self.AddToken(aux)

            elif token.getTag() == Tag.MOD:
                aux = Word('MULOP', Tag.MULOP)
                aux = Word('MULOP', Tag.MULOP)
                #aux = Token(Tag.MULOP)
                self.AddToken(aux)

            # simple_Exprt -> term*
            else:

                aux = Word('simple_Expr', Tag.SIMPLEEXPRESSION)
                #aux = Token(Tag.SIMPLEEXPRESSION)
                self.AddToken(token)
                self.AddToken(aux)

                return b


            token = self.nextToken()
            #print('estado 22')

        return b

    #term-> term mulop *factor_a
    def e23(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            # term -> term mulop factor_a*
            if token.getTag() == Tag.FACTORA:
                aux = Word('TERM', Tag.TERM)
                #aux = Token(Tag.TERM)
                self.AddToken(aux)

                return b

            # factor_a -> *factor
            elif token.getTag() == Tag.FACTOR:
                aux = Word('FACTOR-A', Tag.FACTORA)
                #aux = Token(Tag.FACTORA)
                self.AddToken(aux)

            # factor_a -> *not factor
            elif token.getTag() == Tag.NOT:
                b = self.e21() and b

            # factor_a -> *- factor
            elif token.getTag() == Tag.SUB:
                b = self.e31() and b

            #factor -> *identifier
            elif token.getTag() == Tag.ID:
                aux = Word('FACTOR', Tag.FACTOR)
                #aux = Token(Tag.FACTOR)
                self.AddToken(aux)

            # factor -> *constant
            elif token.getTag() == Tag.NUM:
                aux = Word('FACTOR', Tag.FACTOR)
                #aux = Token(Tag.FACTOR)
                self.AddToken(aux)

            # factor -> *(expression)
            elif token.getTag() == Tag.OPAR:
                b = self.e24() and b

            else:

                b = False
                print(f'ERRO! Esperado "id", "numero" ou "(", "not" ou "-", recebido: {token.toString()}')

            token = self.nextToken()
            #print('estado 23')

        return b

    # factor -> (*expression)
    def  e24(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            #factor -> (expression*)
            if token.getTag() == Tag.EXPRESSION:
                b = self.e27() and b
                return b

            # expression -> *simple_Expr
            # expression -> *simple_Expr relop simple_Expr
            # simple_Exprt -> *simple_Expr addop term
            elif token.getTag() == Tag.SIMPLEEXPRESSION:
                b = self.e25() and b

            # simple_Expr -> *term
            # term -> *term mulop factor_a
            elif token.getTag() == Tag.TERM:
                b = self.e22() and b

            # simple_Expr -> ? simple_Expr : simple_Expr
            # factor -> *(expression)
            elif token.getTag() == Tag.OPAR:
                b = self.e45() and b

            # term -> *factor_a
            elif token.getTag() == Tag.FACTORA:
                aux = Word('TERM', Tag.TERM)
                aux = Token(Tag.TERM)
                self.AddToken(aux)

            # factor_a -> *factor
            elif token.getTag() == Tag.FACTOR:
                aux = Word('FACTOR-A', Tag.FACTORA)
                #aux = Token(Tag.FACTORA)
                self.AddToken(aux)

            # factor_a -> *not factor
            elif token.getTag() == Tag.NOT:
                b = self.e21() and b

            # factor_a -> *- factor
            elif token.getTag() == Tag.SUB:
                b = self.e31() and b

            elif token.getTag() == Tag.ID:
                aux = Word('FACTOR', Tag.FACTOR)
                #aux = Token(Tag.FACTOR)
                self.AddToken(aux)

            # factor -> *constant
            elif token.getTag() == Tag.NUM:
                aux = Word('FACTOR', Tag.FACTOR)
                #aux = Token(Tag.FACTOR)
                self.AddToken(aux)

            else:

                b = False
                print(f'ERRO! Esperado "identifier", "numero", "(", "not" ou "-", recebido: {token.toString()}, '
                      f'{token.getTag()}')

            token = self.nextToken()
            #print('estado 24')


        return b

    # expression -> simple_Expr*
    # expression -> simple_Expr* relop simple_Expr
    # simple_Exprt -> simple_Expr* addop term
    def e25(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            # expression -> simple_Expr relop* simple_Expr
            if token.getTag() == Tag.RELOP:
                b = self.e26() and b
                return b

            # simple_Expr -> simple_Expr addop* term
            elif token.getTag() == Tag.ADDOP:
                b = self.e28() and b
                return b

            elif token.getTag() == Tag.EQ:
                aux = Word('RELOP', Tag.RELOP)
                #aux = Token(Tag.RELOP)
                self.AddToken(aux)

            elif token.getTag() == Tag.GT:
                aux = Word('RELOP', Tag.RELOP)
                #aux = Token(Tag.RELOP)
                self.AddToken(aux)

            elif token.getTag() == Tag.GE:
                aux = Word('RELOP', Tag.RELOP)
                #aux = Token(Tag.RELOP)
                self.AddToken(aux)

            elif token.getTag() == Tag.LT:
                aux = Word('RELOP', Tag.RELOP)
                #aux = Token(Tag.RELOP)
                self.AddToken(aux)

            elif token.getTag() == Tag.LE:
                aux = Word('RELOP', Tag.RELOP)
                #aux = Token(Tag.RELOP)
                self.AddToken(aux)

            elif token.getTag() == Tag.NE:
                aux = Word('RELOP', Tag.RELOP)
                #aux = Token(Tag.RELOP)
                self.AddToken(aux)

            elif token.getTag() == Tag.ADD:
                aux = Word('ADDOP', Tag.ADDOP)
                #aux = Token(Tag.ADDOP)
                self.AddToken(aux)

            elif token.getTag() == Tag.SUB:
                aux = Word('ADDOP', Tag.ADDOP)
                #aux = Token(Tag.ADDOP)
                self.AddToken(aux)

            elif token.getTag() == Tag.OR:
                aux = Word('ADDOP', Tag.ADDOP)
                #aux = Token(Tag.ADDOP)
                self.AddToken(aux)

            else:

                aux = Token(Tag.EXPRESSION)
                self.AddToken(token)
                self.AddToken(aux)

                return b

            token = self.nextToken()
            #print('estado 24')

        return b

    #expression -> simple_Expr relop *simple_Expr
    def e26(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            # expression -> simple_Expr relop *simple_Expr
            # simple_Expr -> *simple_Expr *addop simple_Expr
            if token.getTag() == Tag.SIMPLEEXPRESSION:
                b = self.e29() and b
                return b

            # simple_Expr -> *term
            # term -> *term mulop factor_a
            elif token.getTag() == Tag.TERM:
                b = self.e22() and b

            # simple_Expr -> (simple_Expr) ? simple_Expr : simple_Expr
            # factor -> *(expression)
            elif token.getTag() == Tag.OPAR:
                b = self.e45() and b

            # term -> *factor_a
            elif token.getTag() == Tag.FACTORA:
                aux = Word('TERM', Tag.TERM)
                #aux = Token(Tag.TERM)
                self.AddToken(aux)

            # factor_a -> *factor
            elif token.getTag() == Tag.FACTOR:
                aux = Word('FACTOR-A', Tag.FACTORA)
                #aux = Token(Tag.FACTORA)
                self.AddToken(aux)

            # factor_a -> *not factor
            elif token.getTag() == Tag.NOT:
                b = self.e21() and b

            # factor_a -> *not factor
            elif token.getTag() == Tag.SUB:
                b = self.e31() and b

            elif token.getTag() == Tag.ID:
                aux = Word('FACTOR', Tag.FACTOR)
                #aux = Token(Tag.FACTOR)
                self.AddToken(aux)

            # factor -> *constant
            elif token.getTag() == Tag.NUM:
                aux = Word('FACTOR', Tag.FACTOR)
                #aux = Token(Tag.FACTOR)
                self.AddToken(aux)

            else:

                b = False
                print(f'ERRO! Esperado "id", "numero" ou "(", "not" ou "-", recebido: {token.toString()}')

            token = self.nextToken()

        return b

    # factor -> ( expression *)
    def e27(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            if token.getTag() == Tag.CPAR:

                aux = Word('FACTOR', Tag.FACTOR)
                #aux = Token(Tag.FACTOR)
                self.AddToken(aux)

                return b

            else:
                b = False
                print(f'ERRO! Esperado ")" recebido, {token.toString()}')

            token = self.nextToken()
            #print('estado 27')

        return b

    # simple_Expr -> simple_Expr addop *term
    def e28(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            # simple_Expr -> simple_Expr addop *term
            # term -> *term mulop factor_a
            if token.getTag() == Tag.TERM:
                b = self.e30() and b

                return b

            #factor -> *(expression)
            elif token.getTag() == Tag.OPAR:
                b = self.e24() and b

            #term -> *factor_a
            elif  token.getTag() == Tag.FACTORA:
                aux = Word('TERM', Tag.TERM)
                #aux = Token(Tag.TERM)
                self.AddToken(aux)

            #factor_a -> *factor
            elif token.getTag() == Tag.FACTOR:
                aux = Word('FACTOR-A', Tag.FACTORA)
                #aux = Token(Tag.FACTORA)
                self.AddToken(aux)

            # factor_a -> *not factor
            elif token.getTag() == Tag.NOT:
                b = self.e21() and b

            # factor_a -> *- factor
            elif token.getTag() == Tag.SUB:
                b = self.e31() and b

            elif token.getTag() == Tag.ID:
                aux = Word('FACTOR', Tag.FACTOR)
                #aux = Token(Tag.FACTOR)
                self.AddToken(aux)

            #factor -> *constant
            elif token.getTag() == Tag.NUM:
                aux = Word('FACTOR', Tag.FACTOR)
                #aux = Token(Tag.FACTOR)
                self.AddToken(aux)

            # assign-stmt -> *identifier := simple_Expr
            elif token.getTag() == Tag.ID:
                b = self.e17() and b

            else:
                b = False
                print(f'ERRO! Esperado "id", "numero" ou "(", "not" ou "-", recebido: {token.toString()}')

            token = self.nextToken()
            #print('estado 28')

        return  b

    # expression -> simple_Expr relop simple_Expr*
    # simple_Expr -> simple_Expr *addop term
    def e29(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            # term -> term mulop* factor_a
            if token.getTag() == Tag.ADDOP:
                b = self.e28() and b
                return b

            elif token.getTag() == Tag.ADD:
                aux = Word('ADDOP', Tag.ADDOP)
                #aux = Token(Tag.ADDOP)
                self.AddToken(aux)

            elif token.getTag() == Tag.SUB:
                aux = Word('ADDOP', Tag.ADDOP)
                aux = Token(Tag.ADDOP)
                self.AddToken(aux)


            elif token.getTag() == Tag.OR:
                aux = Word('ADDOP', Tag.ADDOP)
                aux = Token(Tag.ADDOP)
                self.AddToken(aux)


            else:

                aux = Word('EXPRESSION', Tag.EXPRESSION)
                #aux = Token(Tag.EXPRESSION)
                self.AddToken(token)
                self.AddToken(aux)

                return b

            token = self.nextToken()

            #print('estado 24')

        return b

    # simple_Expr -> simple_Expr addop term*
    # term -> term * mulop factor_a
    def  e30(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            # term -> term mulop* factor_a
            if token.getTag() == Tag.MULOP:
                b = self.e23() and b
                return b

            elif token.getTag() == Tag.MLT:
                aux = Word('MULOP', Tag.MULOP)
                #aux = Token(Tag.MULOP)
                self.AddToken(aux)

            elif token.getTag() == Tag.DIV:
                aux = Word('MULOP', Tag.MULOP)
                #aux = Token(Tag.MULOP)
                self.AddToken(aux)

            elif token.getTag() == Tag.AND:
                aux = Word('MULOP', Tag.MULOP)
                #aux = Token(Tag.MULOP)
                self.AddToken(aux)

            elif token.getTag() == Tag.MOD:
                aux = Word('MULOP', Tag.MULOP)
                #aux = Token(Tag.MULOP)
                self.AddToken(aux)

            # simple_Expr -> simple_Expr addop term*
            else:

                aux = Word('simple_Expr', Tag.SIMPLEEXPRESSION)
                aux = Token(Tag.SIMPLEEXPRESSION)
                self.AddToken(token)
                self.AddToken(aux)

                return b

            token = self.nextToken()
            #print('estado 30')

        return b

    #factor_a -> *- factor
    def e31(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            # factor_a -> - *factor
            if token.getTag() == Tag.FACTOR:
                aux = Word('FACTOR-A', Tag.FACTORA)
                #aux = Token(Tag.FACTORA)
                self.AddToken(aux)
                return b

            # factor -> *identifier
            elif token.getTag() == Tag.ID:
                aux = Word('FACTOR', Tag.FACTOR)
                #aux = Token(Tag.FACTOR)
                self.AddToken(aux)

            # factor -> *constant
            elif token.getTag() == Tag.NUM:
                aux = Word('FACTOR', Tag.FACTOR)
                #aux = Token(Tag.FACTOR)
                self.AddToken(aux)

            # factor -> *(expression)
            elif token.getTag() == Tag.OPAR:
                b = self.e21() and b

            else:
                b = False
                print(f'ERRO! Esperado "id", "numero" ou "(", recebido: {token.toString()}')

            token = self.nextToken()

        return b

    #body -> begin stmt-list *end
    #body -> declare dec-lst begin stmt-list *end
    def e32(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            if token.getTag() == Tag.END:
                aux = Word('BODY', Tag.BODY)
                #aux = Token(Tag.BODY)
                self.AddToken(aux)
                return b

            else:
                b = False
                print(f'ERRO! Esperado "end", recebido: {token.toString()}')


            token = self.nextToken()

        return b

    #S -> programa id body * $
    def e33(self):

        b = True

        token = self.nextToken()

        if token.getTag() == Tag.FIM:
            aux = Word('S', Tag.S)
            #aux = Token(Tag.S)
            self.AddToken(aux)

        else:
            b = False
            print(f'ERRO! Esperado "fim de arquivo", recebido: {token.toString()}')

        return b

    # writable -> simple_Expr*
    # simple_Expr -> simple_Expr *addop term
    def e34(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            # simple_Expr -> simple_Expr *addop term
            if token.getTag() == Tag.ADDOP:
                b = self.e28() and b
                return b

            elif token.getTag() == Tag.ADD:
                aux = Word('ADDOP', Tag.ADDOP)
                #aux = Token(Tag.ADDOP)
                self.AddToken(aux)


            elif token.getTag() == Tag.SUB:
                aux = Word('ADDOP', Tag.ADDOP)
                #aux = Token(Tag.ADDOP)
                self.AddToken(aux)


            elif token.getTag() == Tag.OR:
                aux = Word('ADDOP', Tag.ADDOP)
                #aux = Token(Tag.ADDOP)
                self.AddToken(aux)

            else:
                aux = Word('WRITEABLE', Tag.WRITEABLE)
                #aux = Token(Tag.WRITEABLE)
                self.AddToken(token)
                self.AddToken(aux)

                return b

            token = self.nextToken()

        return b

    # do-while-stmt -> do * stmt-list stmt-suffix
    def e35(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            # do-while-stmt -> do stmt-list* stmt-suffix
            if token.getTag() == Tag.STMTLST:
                b = self.e36() and b
                return b

            # stmt-list -> *stmt; [stmt;]
            elif token.getTag() == Tag.STMT:
                b = self.e19()

            # stmt -> assign-stmt
            elif token.getTag() == Tag.ASSIGNSTMT:
                aux = Word('STMT', Tag.STMT)
                #aux = Token(Tag.STMT)
                self.AddToken(aux)

            # stmt -> if-stmt
            elif token.getTag() == Tag.IFSTMT:
                aux = Word('STMT', Tag.STMT)
                # aux = Token(Tag.STMT)
                self.AddToken(aux)

            # stmt -> *do-while-stmt
            elif token.getTag() == Tag.DOWHILESTMT:
                aux = Word('STMT', Tag.STMT)
                #aux = Token(Tag.STMT)
                self.AddToken(aux)

            # stmt -> *readstmt
            elif token.getTag() == Tag.READSTMT:
                aux = Word('STMT', Tag.STMT)
                #aux = Token(Tag.STMT)
                self.AddToken(aux)

            # stmt => write-stmt
            elif token.getTag() == Tag.WRITESTMT:
                aux = Word('STMT', Tag.STMT)
                #aux = Token(Tag.STMT)
                self.AddToken(aux)

            # assign-stmt -> *identifier := simple_Expr
            elif token.getTag() == Tag.ID:
                self.e17()

            # if-stmt -> *if condition then stmt-list end
            # if-stmt -> *if condition then stmt-list else stm-list end
            elif token.getTag() == Tag.IF:
                b = self.e39() and b

            #do-while -> *do stmt-list stmt-suffix
            elif token.getTag() == Tag.DO:
                self.e35()

            # read-stmt -> *read(identifier)
            elif token.getTag() == Tag.READ:
                b = self.e11() and b

            # write-stmt -> *write(writable)
            elif token.getTag() == Tag.WRITE:
                b = self.e12() and b

            else:
                b = False
                print(f'ERRO! Esperado "identifier", "if" ou "while", "read" ou "write", recebido: {token.toString()}')

            token = self.nextToken()

        return b

    # do-while-stmt -> do stmt-list* stmt-suffix
    def e36(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            #do-while-stmt -> do stmt-list *stmt-suffix
            if token.getTag() == Tag.STMTSUFFIX:
                aux = Word('DOWHILESTMT', Tag.DOWHILESTMT)
                #aux = Token(Tag.DOWHILESTMT)
                self.AddToken(aux)
                return b

            #stmt-suffix -> *while condition
            elif token.getTag() == Tag.WHILE:
                b = self.e37() and b

            else:
                b = False
                print(f'ERRO! Esperado "while" recebido {token.toString()}')

            token = self.nextToken()


        return b

    #stmt-suffix -> while* condition
    def e37(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            if token.getTag() == Tag.CONDITION:
                aux = Word('STMTSUFFIX', Tag.STMTSUFFIX)
                #aux = Token(Tag.STMTSUFFIX)
                self.AddToken(aux)
                return b

            #codition -> *expression
            elif token.getTag() == Tag.EXPRESSION:
                aux = Word('CONDITION', Tag.CONDITION)
                #aux = Token(Tag.CONDITION)
                self.AddToken(aux)

            # expression -> *simple_Expr
            # expression -> *simple_Expr relop simple_Expr
            # simple_Exprt -> *simple_Expr addop simple_Expr
            elif token.getTag() == Tag.SIMPLEEXPRESSION:
                b = self.e25() and b


            # simple_Expr -> *term
            # term -> *term mulop factor_a
            elif token.getTag() == Tag.TERM:
                b = self.e22() and b

            # simple_Expr -> *(simple_Expr) ? simple_Expr : simple_Expr
            # factor -> *(expression)
            elif token.getTag() == Tag.OPAR:
                b = self.e45() and b

            # term -> *factor_a
            elif token.getTag() == Tag.FACTORA:
                aux = Token(Tag.TERM)
                self.AddToken(aux)

            # factor_a -> *factor
            elif token.getTag() == Tag.FACTOR:
                aux = Token(Tag.FACTORA)
                self.AddToken(aux)

            # factor_a -> *not factor
            elif token.getTag() == Tag.NOT:
                b = self.e21() and b

            # factor_a -> *not factor
            elif token.getTag() == Tag.SUB:
                b = self.e31() and b

            elif token.getTag() == Tag.ID:
                aux = Word('FACTOR', Tag.FACTOR)
                #aux = Token(Tag.FACTOR)
                self.AddToken(aux)

            # factor -> *constant
            elif token.getTag() == Tag.NUM:
                aux = Word('FACTOR', Tag.FACTOR)
                #aux = Token(Tag.FACTOR)
                self.AddToken(aux)

            else:
                b = False
                print(f'ERRO! Esperado "identifier", "numero" ou "(", "not" ou "-", recebido: {token.toString()}')

            token = self.nextToken()

        return b


    #assignt-stmt -> identifier := simple_Expr*
    #simple-Expr -> simple_Expr *addop simple_Expr
    def e38(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            # simple_Expr -> simple_Expr addop* term
            if token.getTag() == Tag.ADDOP:
                b = self.e28() and b

                token = self.nextToken()
                aux = Word('ASSIGNSTMT', Tag.ASSIGNSTMT)
                #aux = Token(Tag.ASSIGNSTMT)
                self.AddToken(aux)

                return b

            elif token.getTag() == Tag.ADD:
                aux = Word('ADDOP', Tag.ADDOP)
                #aux = Token(Tag.ADDOP)
                self.AddToken(aux)

            elif token.getTag() == Tag.SUB:
                aux = Word('ADDOP', Tag.ADDOP)
                #aux = Token(Tag.ADDOP)
                self.AddToken(aux)

            elif token.getTag() == Tag.OR:
                aux = Word('ADDOP', Tag.ADDOP)
                #aux = Token(Tag.ADDOP)
                self.AddToken(aux)

            else:
                aux = Word('ASSIGNSTMT', Tag.ASSIGNSTMT)
                #aux = Token(Tag.ASSIGNSTMT)
                self.AddToken(token)
                self.AddToken(aux)

                return b

            token = self.nextToken()

        return b

    # if-stmt -> if* condition then stmt-list end
    # if-stmt -> if* condition then stmt-list else stm-list end
    def e39(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            if token.getTag() == Tag.CONDITION:
                b = self.e40() and b
                return b

            #codition -> *expression
            elif token.getTag() == Tag.EXPRESSION:
                aux = Word('CONDITION', Tag.CONDITION)
                #aux = Token(Tag.CONDITION)
                self.AddToken(aux)

            # expression -> *simple_Expr
            # expression -> *simple_Expr relop simple_Expr
            # simple_Exprt -> *simple_Expr addop simple_Expr
            elif token.getTag() == Tag.SIMPLEEXPRESSION:
                b = self.e25() and b

            # simple_Expr -> *term
            # term -> *term mulop factor_a
            elif token.getTag() == Tag.TERM:
                b = self.e22() and b

            # factor -> *(expression)
            # simple_Expr -> *(simple_Expr) ? simple_Expr : simple_Expr
            elif token.getTag() == Tag.OPAR:
                b = self.e45() and b

            # term -> *factor_a
            elif token.getTag() == Tag.FACTORA:
                aux = Word('TERM', Tag.TERM)
                #aux = Token(Tag.TERM)
                self.AddToken(aux)

            # factor_a -> *factor
            elif token.getTag() == Tag.FACTOR:
                aux = Word('FACTOR-A', Tag.FACTORA)
                #aux = Token(Tag.FACTORA)
                self.AddToken(aux)

            # factor_a -> *not factor
            elif token.getTag() == Tag.NOT:
                b = self.e21() and b

            # factor_a -> *not factor
            elif token.getTag() == Tag.SUB:
                b = self.e31() and b

            # factor_a -> identifier
            elif token.getTag() == Tag.ID:
                aux = Word('FACTOR', Tag.FACTOR)
                # aux = Token(Tag.FACTOR)
                self.AddToken(aux)

            # factor -> *constant
            elif token.getTag() == Tag.NUM:
                aux = Word('FACTOR', Tag.FACTOR)
                #aux = Token(Tag.FACTOR)
                self.AddToken(aux)

            else:
                b = False
                print(f'ERRO! Esperado "identifier", "numero" ou "(", "not" ou "-", recebido: {token.toString()}')

            token = self.nextToken()

        return b

    # if-stmt -> if condition *then stmt-list end
    # if-stmt -> if condition *then stmt-list else stm-list end
    def e40(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            # term -> term mulop* factor_a
            if token.getTag() == Tag.THEN:
                b = self.e41() and b
                return b

            else:

                b = False
                print(f'ERRO! Esperado "then" recebido {token.toString()}')

            token = self.nextToken()

            #print('estado 40')

        return b

    # if-stmt -> if condition then* stmt-list end
    # if-stmt -> if condition then* stmt-list else stm-list end
    def e41(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            if token.getTag() == Tag.STMTLST:
                b = self.e42() and b
                return b

            #stmt-list -> *stmt; [stmt;]
            elif token.getTag() == Tag.STMT:
                b = self.e19() and b

            #stmt -> assign-stmt
            elif token.getTag() == Tag.ASSIGNSTMT:
                aux = Word('STMT', Tag.STMT)
                #aux = Token(Tag.STMT)
                self.AddToken(aux)

            # stmt -> if-stmt
            elif token.getTag() == Tag.IFSTMT:
                aux = Word('STMT', Tag.STMT)
                #aux = Token(Tag.STMT)
                self.AddToken(aux)

            # stmt -> do-while-stmt
            elif token.getTag() == Tag.DOWHILESTMT:
                aux = Word('STMT', Tag.STMT)
                #aux = Token(Tag.STMT)
                self.AddToken(aux)

            # stmt -> *readstmt
            elif token.getTag() == Tag.READSTMT:
                aux = Word('STMT', Tag.STMT)
                #aux = Token(Tag.STMT)
                self.AddToken(aux)

            # stmt => write-stmt
            elif token.getTag() == Tag.WRITESTMT:
                aux = Word('STMT', Tag.STMT)
                #aux = Token(Tag.STMT)
                self.AddToken(aux)

            # assign-stmt -> *identifier := simple_Expr
            elif token.getTag() == Tag.ID:
                self.e17()

            # if-stmt -> *if condition then stmt-list end
            # if-stmt -> *if condition then stmt-list else stm-list end
            elif token.getTag() == Tag.IF:
                b = self.e39() and b

            # do-while-stmt -> *do stmt-list stmt-suffix
            elif token.getTag() == Tag.DO:
                b = self.e35() and b

            #read-stmt -> *read(identifier)
            elif token.getTag() == Tag.READ:
                b = self.e11() and b

            #write-stmt -> *write(writable)
            elif token.getTag() == Tag.WRITE:
                b = self.e12() and b

            else:
                b = False
                print(f'ERRO! Esperado "identifier", "if" ou "while", "read" ou "write", recebido: {token.toString()}')

            token = self.nextToken()

        return  b

    # if-stmt -> *if condition then stmt-list* end
    # if-stmt -> *if condition then stmt-list* else stm-list end
    def e42(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            # if-stmt -> *if condition then stmt-list* end
            if token.getTag() == Tag.END:
                aux = Word('IFSTMT', Tag.IFSTMT)
                #aux = Token(Tag.IFSTMT)
                self.AddToken(aux)
                return b

            # if-stmt -> *if condition then stmt-list* else stmt-list end
            elif token.getTag() == Tag.ELSE:
                b = self.e43() and b
                return b

            else:

                b = False
                print(f'Erro! Esperado "end" ou "else", recebido {token.toString()}')

            token = self.nextToken()

            #print('estado 42')

        return b

    # if-stmt -> if condition then stmt-list else *stm-list end
    def e43(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            if token.getTag() == Tag.STMTLST:
                b = self.e44() and b
                return b

            #stmt-list -> *stmt; [stmt;]
            elif token.getTag() == Tag.STMT:
                b = self.e19() and b

            #stmt -> assign-stmt
            elif token.getTag() == Tag.ASSIGNSTMT:
                aux = Word('STMT', Tag.STMT)
                #aux = Token(Tag.STMT)
                self.AddToken(aux)

            #stmt -> if-stmt
            elif token.getTag() == Tag.IFSTMT:
                aux = Word('STMT', Tag.STMT)
                #aux = Token(Tag.STMT)
                self.AddToken(aux)

            #stmt -> do-while-stmt
            elif token.getTag() == Tag.DOWHILESTMT:
                aux = Word('STMT', Tag.STMT)
                #aux = Token(Tag.STMT)
                self.AddToken(aux)

            # stmt -> *readstmt
            elif token.getTag() == Tag.READSTMT:
                aux = Word('STMT', Tag.STMT)
                #aux = Token(Tag.STMT)
                self.AddToken(aux)

            # stmt => write-stmt
            elif token.getTag() == Tag.WRITESTMT:
                aux = Word('STMT', Tag.STMT)
                #aux = Token(Tag.STMT)
                self.AddToken(aux)

            # assign-stmt -> *identifier := simple_Expr
            elif token.getTag() == Tag.ID:
                b = self.e17() and b

            # if-stmt -> *if condition then stmt-list end
            # if-stmt -> *if condition then stmt-list else stm-list end
            elif token.getTag() == Tag.IF:
                b = self.e39() and b

            # do-while-stmt -> *do stmt-list stmt-suffix
            elif token.getTag() == Tag.DO:
                b = self.e35() and b

            #read-stmt -> *read(identifier)
            elif token.getTag() == Tag.READ:
                b = self.e11() and b

            #write-stmt -> *write(writable)
            elif token.getTag() == Tag.WRITE:
                b = self.e12() and b

            else:
                b = False
                print(f'ERRO! Esperado "identifier", "if" ou "while", "read" ou "write", recebido: {token.toString()}')

            token = self.nextToken()

        return  b

    # if-stmt -> if condition then stmt-list else stm-list *end
    def e44(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            # if-stmt -> *if condition then stmt-list else stmt-list end*
            if token.getTag() == Tag.END:
                aux = Word('IFSTMT', Tag.IFSTMT)
                #aux = Token(Tag.IFSTMT)
                self.AddToken(aux)
                return b

            else:

                b = False
                print(f'Erro! Esperado "end", recebido {token.toString()}')

            token = self.nextToken()

            #print('estado 44')

        return b

    # simple_Expr -> (*simple_Expr) ? simple_Expr : simple_Expr
    # factor -> (*expression)
    def e45(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            if token.getTag() == Tag.EXPRESSION:

                follow = self.nextToken()

                if follow.getTag() == Tag.SMC:

                    aux = Word('SIMPLEEXPRESSION', Tag.SIMPLEEXPRESSION)
                    self.AddToken(follow)
                    self.AddToken(aux)

                    return b

                self.AddToken(follow)
                b = self.e27() and b
                return b

            # expression -> *simple_Expr
            # expression -> *simple_Expr relop simple_Expr
            # simple_Expr -> (*simple_Expr) ? simple_Expr : simple_Expr
            # simple_Exprt -> *simple_Expr addop term
            elif token.getTag() == Tag.SIMPLEEXPRESSION:
                b = self.e46() and b

            # simple_Expr -> *term
            # term -> *term mulop factor_a
            elif token.getTag() == Tag.TERM:
                b = self.e22() and b

            # simple_Expr -> *(simple_Expr) ? simple_Expr : simple_Expr
            # factor -> *(expression)
            elif token.getTag() == Tag.OPAR:
                b = self.e45() and b

            # term -> *factor_a
            elif token.getTag() == Tag.FACTORA:
                aux = Word('TERM', Tag.TERM)
                #aux = Token(Tag.TERM)
                self.AddToken(aux)

            # factor_a -> *factor
            elif token.getTag() == Tag.FACTOR:
                aux = Word('FACTOR-A', Tag.FACTORA)
                #aux = Token(Tag.FACTORA)
                self.AddToken(aux)

            # factor_a -> *not factor
            elif token.getTag() == Tag.NOT:
                b = self.e21() and b

            # factor_a -> *- factor
            elif token.getTag() == Tag.SUB:
                b = self.e31() and b

            elif token.getTag() == Tag.ID:
                aux = Word('FACTOR', Tag.FACTOR)
                #aux = Token(Tag.FACTOR)
                self.AddToken(aux)

            # factor -> *constant
            elif token.getTag() == Tag.NUM:
                aux = Word('FACTOR', Tag.FACTOR)
                #aux = Token(Tag.FACTOR)
                self.AddToken(aux)

            else:
                b = False
                print(f'ERRO! Esperado "identifier", "numero" ou "(", "not" ou "-", recebido: {token.toString()}')

            token = self.nextToken()
            #print('estado 45')

        return b


    # expression -> simple_Expr*
    # expression -> simple_Expr* relop simple_Expr
    # simple_Expr -> (simple_Expr*) ? simple_Expr : simple_Expr
    # simple_Expr -> simple_Expr* addop term
    def e46(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            # expression -> simple_Expr relop* simple_Expr
            if token.getTag() == Tag.RELOP:
                b = self.e26() and b
                return b

            # simple_Expr -> (simple_Expr*) ? simple_Expr : simple_Expr
            elif token.getTag() == Tag.CPAR:

                follow = self.nextToken()

                if follow.getTag() != Tag.QST:

                    self.AddToken(follow)
                    self.AddToken(token)

                    aux = Word('EXPRESSION', Tag.EXPRESSION)
                    self.AddToken(aux)

                    return b

                self.AddToken(follow)
                b = self.e47() and b

                return b

            # simple_Expr -> simple_Expr addop* term
            elif token.getTag() == Tag.ADDOP:
                b = self.e28() and b
                return b

            elif token.getTag() == Tag.EQ:
                aux = Word('RELOP', Tag.RELOP)
                #aux = Token(Tag.RELOP)
                self.AddToken(aux)

            elif token.getTag() == Tag.GT:
                aux = Word('RELOP', Tag.RELOP)
                #aux = Token(Tag.RELOP)
                self.AddToken(aux)

            elif token.getTag() == Tag.GE:
                aux = Word('RELOP', Tag.RELOP)
                #aux = Token(Tag.RELOP)
                self.AddToken(aux)

            elif token.getTag() == Tag.LT:
                aux = Word('RELOP', Tag.RELOP)
                #aux = Token(Tag.RELOP)
                self.AddToken(aux)

            elif token.getTag() == Tag.LE:
                aux = Word('RELOP', Tag.RELOP)
                #aux = Token(Tag.RELOP)
                self.AddToken(aux)

            elif token.getTag() == Tag.NE:
                aux = Word('RELOP', Tag.RELOP)
                #aux = Token(Tag.RELOP)
                self.AddToken(aux)

            elif token.getTag() == Tag.ADD:
                aux = Word('ADDOP', Tag.ADDOP)
                #aux = Token(Tag.ADDOP)
                self.AddToken(aux)

            elif token.getTag() == Tag.SUB:
                aux = Word('ADDOP', Tag.ADDOP)
                #aux = Token(Tag.ADDOP)
                self.AddToken(aux)

            elif token.getTag() == Tag.OR:
                aux = Word('ADDOP', Tag.ADDOP)
                #aux = Token(Tag.ADDOP)
                self.AddToken(aux)

            else:
                aux = Word('EXPRESSION', Tag.EXPRESSION)
                #aux = Token(Tag.EXPRESSION)
                self.AddToken(token)
                self.AddToken(aux)

                return b

            token = self.nextToken()

        return b

    # simple_Expr -> (simple_Expr ) *? simple_Expr : simple_Expr
    def e47(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            if token.getTag() == Tag.QST:
                b = self.e48() and b
                return b
            else:
                b = False
                print(f'ERRO! Esperado "?", recebido: {token.toString()}')

            token = self.nextToken()


        return b


    # simple_Expr -> (simple_Expr) ?* simple_Expr : simple_Expr
    def e48(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            # simple_Expr -> (simple_Expr) ?* simple_Expr : simple_Expr
            # simple_Exprt -> *simple_Expr addop term
            if token.getTag() == Tag.SIMPLEEXPRESSION:
                b = self.e49() and b
                return b

            # simple_Expr -> *term
            # term -> *term mulop factor_a
            elif token.getTag() == Tag.TERM:
                b = self.e22() and b

            # simple_Expr -> *(simple_Expr) ? simple_Expr : simple_Expr
            # factor -> *(expression)
            elif token.getTag() == Tag.OPAR:
                b = self.e45() and b

            # term -> *factor_a
            elif token.getTag() == Tag.FACTORA:
                aux = Word('TERM', Tag.TERM)
                #aux = Token(Tag.TERM)
                self.AddToken(aux)

            # factor_a -> *factor
            elif token.getTag() == Tag.FACTOR:
                aux = Word('FACTOR-A', Tag.FACTORA)
                #aux = Token(Tag.FACTORA)
                self.AddToken(aux)

            # factor_a -> *not factor
            elif token.getTag() == Tag.NOT:
                b = self.e21() and b

            # factor_a -> *- factor
            elif token.getTag() == Tag.SUB:
                b = self.e31() and b

            elif token.getTag() == Tag.ID:
                aux = Word('FACTOR', Tag.FACTOR)
                #aux = Token(Tag.FACTOR)
                self.AddToken(aux)

            # factor -> *constant
            elif token.getTag() == Tag.NUM:
                aux = Word('FACTOR', Tag.FACTOR)
                #aux = Token(Tag.FACTOR)
                self.AddToken(aux)

            else:
                b = False
                print(f'ERRO! Esperado "id", "numero" ou "(", "not" ou "-", recebido: {token.toString()}')

            token = self.nextToken()
            #print('estado 48')

        return b

    # simple_Expr -> (simple_Expr) ? simple_Expr* : simple_Expr
    # simple_Expr -> simple_Expr *addop term
    def e49(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            # simple_Expr -> (simple_Expr) ? simple_Expr* : simple_Expr
            if token.getTag() == Tag.CLM:
                b = self.e50() and b
                return b

            # term -> term mulop* factor_a
            elif token.getTag() == Tag.ADDOP:
                b = self.e28() and b
                return b

            elif token.getTag() == Tag.ADD:
                aux = Word('ADDOP', Tag.ADDOP)
                #aux = Token(Tag.ADDOP)
                self.AddToken(aux)


            elif token.getTag() == Tag.SUB:
                aux = Word('ADDOP', Tag.ADDOP)
                #aux = Token(Tag.ADDOP)
                self.AddToken(aux)


            elif token.getTag() == Tag.OR:
                aux = Word('ADDOP', Tag.ADDOP)
                #aux = Token(Tag.ADDOP)
                self.AddToken(aux)

            else:
                b = False
                print(f'ERRO! Esperado ":", "+", "-" ou "or", recebido: {token.toString()}')

            token = self.nextToken()

            #print('estado 49')

        return b

    # simple_Expr -> (simple_Expr) ? simple_Expr : *simple_Expr
    def e50(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            # simple_Expr -> (simple_Expr) ? simple_Expr : *simple_Expr
            # simple_Exprt -> *simple_Expr addop term
            if token.getTag() == Tag.SIMPLEEXPRESSION:
                #(token.toString())
                b = self.e51() and b

                return b

            # simple_Expr -> *term
            # term -> *term mulop factor_a
            elif token.getTag() == Tag.TERM:
                b = self.e22() and b

            # simple_Expr -> *(simple_Expr) ? simple_Expr : simple_Expr
            # factor -> *(expression)
            elif token.getTag() == Tag.OPAR:
                b = self.e45() and b

            # term -> *factor_a
            elif token.getTag() == Tag.FACTORA:
                aux = Word('TERM', Tag.TERM)
                #aux = Token(Tag.TERM)
                self.AddToken(aux)

            # factor_a -> *factor
            elif token.getTag() == Tag.FACTOR:
                aux = Word('FACTOR-A', Tag.FACTORA)
                #aux = Token(Tag.FACTORA)
                self.AddToken(aux)

            # factor_a -> *not factor
            elif token.getTag() == Tag.NOT:
                b = self.e21() and b

            # factor_a -> *- factor
            elif token.getTag() == Tag.SUB:
                b = self.e31() and b

            elif token.getTag() == Tag.ID:
                aux = Word('FACTOR', Tag.FACTOR)
                #aux = Token(Tag.FACTOR)
                self.AddToken(aux)

            # factor -> *constant
            elif token.getTag() == Tag.NUM:
                aux = Word('FACTOR', Tag.FACTOR)
                #aux = Token(Tag.FACTOR)
                self.AddToken(aux)

            else:
                b = False
                print(f'ERRO! Esperado "identifier", "numero", "(", "not" ou "-", recebido: {token.toString()}')

            token = self.nextToken()

        return b

    # simple_Expr -> (simple_Expr) ? simple_Expr : *simple_Expr
    # simple_Expr -> simple_Expr *addop term
    def e51(self):

        b = True

        token = self.nextToken()

        while token.getTag() != Tag.FIM:

            # term -> term mulop* factor_a
            if token.getTag() == Tag.ADDOP:
                b = self.e28() and b
                return b

            elif token.getTag() == Tag.ADD:
                aux = Word('ADDOP', Tag.ADDOP)
                #aux = Token(Tag.ADDOP)
                self.AddToken(aux)

            elif token.getTag() == Tag.SUB:
                aux = Word('ADDOP', Tag.ADDOP)
                #aux = Token(Tag.ADDOP)
                self.AddToken(aux)

            elif token.getTag() == Tag.OR:
                aux = Word('ADDOP', Tag.ADDOP)
                #aux = Token(Tag.ADDOP)
                self.AddToken(aux)

            else:

                aux = Word('simple_Expr', Tag.SIMPLEEXPRESSION)
                #aux = Token(Tag.SIMPLEEXPRESSION)
                self.AddToken(token)
                self.AddToken(aux)

                return b

            token = self.nextToken()

            #print('estado 49')

        return b
