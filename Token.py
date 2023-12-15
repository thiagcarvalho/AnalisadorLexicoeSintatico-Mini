from Tag import Tag


class Token:
    def __init__(self, tag=0):
        self.tag = tag

    def getTag(self):
        return self.tag

    def setTag(self, tag):
        self.tag = tag

    def __str__(self):
        if self.tag == Tag.AND:
            return "&&"
        elif self.tag == Tag.DO:
            return "do"
        elif self.tag == Tag.ELSE:
            return "else"
        elif self.tag == Tag.FALSE:
            return "false"
        elif self.tag == Tag.IF:
            return "if"
        elif self.tag == Tag.OR:
            return "||"
        elif self.tag == Tag.READ:
            return "read"
        elif self.tag == Tag.TRUE:
            return "true"
        elif self.tag == Tag.WHILE:
            return "while"
        elif self.tag == Tag.PRG:
            return "program"
        elif self.tag == Tag.MOD:
            return "mod"
        else:
            return str(self.tag)


class Num(Token):
    def __init__(self, val):
        super().__init__(Tag.NUM)
        self.value = val

    def toString(self):
        return str(self.value)


class Word(Token):

    def __init__(self, lex, tag, tipo = None):
        super().__init__(tag)
        self.lexeme = lex
        self.tipo = tipo

    def type(self, tipo):
        self.tipo = tipo
    def toString(self):
        return self.lexeme

    def getTag(self):
        return self.tag

    def getTipo(self):
        return self.tipo

class Words():
    And = Word("and", Tag.AND)
    Or = Word("or", Tag.OR)
    Eq = Word("=", Tag.EQ)
    Gt = Word(">", Tag.GT)
    Ge = Word(">=", Tag.GE)
    Gg = Word(">>>", Tag.GG)
    Ggg = Word(">>>", Tag.GGG)
    Le = Word("<=", Tag.LE)
    Ll = Word("<<", Tag.LL)
    Lll = Word("<<<", Tag.LLL)
    Ne = Word("<>", Tag.NE)
    Lt = Word("<", Tag.LT)

    Mod = Word("mod", Tag.MOD)
    Add = Word("+", Tag.ADD)
    Sub = Word("-", Tag.SUB)
    Mlt = Word("*", Tag.MLT)
    Div = Word("/", Tag.DIV)
    Atrib = Word(":=", Tag.ATRIB)
    Opar = Word("(", Tag.OPAR)
    Cpar = Word(")", Tag.CPAR)
    Smc = Word(";", Tag.SMC)
    """Word.Dqut = Word("\"", Tag.DQUT)
    Word.Pnt = Word(".", Tag.PNT)"""
    Com = Word(",", Tag.COM)
    Qst = Word("?", Tag.QST)
    Clm = Word(":", Tag.CLM)

    # Key Words
    Prog = Word("program", Tag.PRG)
    Beg = Word("begin", Tag.BGN)
    End = Word("end", Tag.END)
    Decl = Word("declare", Tag.DECL)
    true = Word("true", Tag.TRUE)
    false = Word("false", Tag.FALSE)
    If = Word("if", Tag.IF)
    Else = Word("else", Tag.ELSE)
    Then = Word("then", Tag.THEN)
    Do = Word("do", Tag.DO)
    While = Word("while", Tag.WHILE)
    For = Word("for", Tag.FOR)
    Int = Word("integer", Tag.INT)
    Dec = Word("decimal", Tag.DEC)
    Read = Word("read", Tag.READ)
    Write = Word("write", Tag.WRITE)

# Inicialização dos objetos estáticos na classe Word

