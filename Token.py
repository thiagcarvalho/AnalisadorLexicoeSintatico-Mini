from Tag import Tag


class Token:
    def __init__(self, tag):
        self.tag = tag

    def getTag(self):
        return self.tag

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
        else:
            return chr(self.tag)


class Num(Token):
    def __init__(self, val):
        super().__init__(Tag.NUM)
        self.value = val

    def toString(self):
        return str(self.value)


class Word(Token):

    def __init__(self, lex, tag):
        super().__init__(tag)
        self.lexeme = lex

    def toString(self):
        return self.lexeme

class Words():
    And = Word("and", Tag.AND)
    Or = Word("or", Tag.OR)
    """Word.Eq = Word("=", Tag.EQ)
    Word.Ne = Word("<>", Tag.NE)
    Word.Lt = Word("<", Tag.LT)
    Word.Gt = Word(">", Tag.GT)
    Word.Le = Word("<=", Tag.LE)
    Word.Ll = Word("<<", Tag.LL)
    Word.Lll = Word("<<<", Tag.LLL)
    Word.Ge = Word(">=", Tag.GE)
    Word.Gg = Word(">>", Tag.GG)
    Word.Ggg = Word(">>>", Tag.GGG)"""
    Mod = Word("mod", Tag.MOD)
    """Word.Add = Word("+", Tag.ADD)
    Word.Sub = Word("-", Tag.SUB)
    Word.Mlt = Word("*", Tag.MLT)
    Word.Div = Word("/", Tag.DIV)
    Word.Atrib = Word(":=", Tag.ATRIB)
    Word.Opar = Word("(", Tag.OPAR)
    Word.Cpar = Word(")", Tag.CPAR)
    Word.Smc = Word(";", Tag.SMC)
    Word.Dqut = Word("\"", Tag.DQUT)
    Word.Qst = Word("?", Tag.QST)
    Word.Clm = Word(":", Tag.CLM)
    Word.Pnt = Word(".", Tag.PNT)
    Word.Com = Word(",", Tag.COM)"""

    # Key Words
    Prog = Word("program", Tag.PRG)
    # Word.Beg = Word("begin", Tag.BGN)
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

