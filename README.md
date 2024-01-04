## Overview

O repositório apresenta uma implementação, em Python, de um Analisador Léxico, da Tabela de Símbolos e o Analisador Sintático para a linguagem *Mini*, elementos que compõe a etapa inicial de desenvolvimento de um compilador. 
Neste projeto, desenvolvemos uma implementação que realiza simultaneamente os processos de análise léxica e sintática. O sistema é projetado para processar um arquivo de entrada contendo código-fonte, resultando na exibição da saída do Analisador Léxico, 
que inclui a sequência de tokens identificados. Além disso, a análise sintática é conduzida de forma integrada. Ao final do processo, são impressos os símbolos registrados na Tabela de Símbolos, fornecendo uma visão abrangente do fluxo de análise do código.

## Linguagem Mini

A linguagem *Mini* possui a seguinte gramática:

```
program ::= program identifier body
body ::= [declare decl-list] begin stmt-list end
decl-list ::= decl {";" decl}*
decl ::= type ident-list
ident-list ::= identifier {"," identifier}*
type ::= integer | decimal
stmt-list ::= stmt {";" stmt}
stmt ::= assign-stmt | if-stmt | while-stmt
| read-stmt | write-stmt
assign-stmt ::= identifier ":=" simple_expr
if-stmt ::= if condition then stmt-list end
| if condition then stmt-list else stmt-list end
condition ::= expression
do-while-stmt ::= do stmt-list stmt-suffix
stmt-suffix ::= while condition
for-stmt ::= for assign-stmt to condition do stmt-list end //o for é opcional
while-stmt ::= while condition do stmt-list end // o while..do é opcional
read-stmt ::= read "(" identifier ")"
write-stmt ::= write "(" writable ")"
writable ::= simple-expr | literal
expression ::= simple-expr | simple-expr relop simple-expr
simple-expr ::= term | simple-expr addop term | "(" simple-expr ")" ? simple-expr ":" simple-expr
term ::= factor-a | term mulop factor-a
fator-a ::= factor | not factor | "-" factor
factor ::= identifier | constant | "(" expression ")"
relop ::= "=" | ">" | ">=" | "<" | "<=" | "<>"
addop ::= "+" | "-" | or
mulop ::= "*" | "/" | mod | and
shiftop ::= "<<" | ">>" | "<<<" | ">>>"
constant ::= digit {digit}*
literal ::= " “" {caractere} "”"
identifier ::= letter {letter | digit}*
letter ::= "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J"
| "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T"
| "U" | "V" | "W" | "X" | "Y" | "Z" | "a" | "b" | "c" | "d"
| "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n"
| "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x"
| "y" | "z"
digit ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
caractere ::= um dos 256 caracteres do conjunto ASCII, exceto "
```

Algumas outras caractéristicas da linguagem *Mini* são:
* As palavras-chave são reservadas;
* Toda variável deve ser declarada antes do seu uso;
* A semântica dos demais comandos e expressões é a tradicional do Pascal;
* Entrada e saída de Mini estão limitadas ao teclado e à tela de seu computador;
* Comentários de uma linha em Mini começam com \%.

### Implementação do Analisador Léxico 

Para a implementação em Python, primeiro declara-se as palavras reservadas que vão diretamente para a tabela de símbolos, as letras e os dígitos que formarão os *tokens*, então têm-se as funções booleanas que verificarão se são char's válidos ou não.

### Implementação do Analisador Sintático

Na análise sintática, a implementação foi construída com base na máquina de estados. Cada token representa uma transição de estado na estrutura gramatical da linguagem, sendo assim, a análise léxica é necessária. Cada estado é representado por uma 
função booleana que espera o próximo token após o ponto de análise. A verificação do estado é realizada por meio de um loop while que indica o final do arquivo (Tag.FIM) e uma estrutura condicional if que verifica o próximo token recebido.

Se o token for identificado como um redução (*reduce*), o token é retornado; no caso de um *shift*, há uma mudança de estado. Como exemplificado na análise do token '*end*', ocorre um *reduce*, completando a derivação da estrutura *if-stmt* 
ao alcançar o terminal 'end'. Contudo, caso o token seja 'else', o programa é direcionado para outro estado. Como pode ser visto no trecho de código abaixo:

```python

    # read-stmt -> read(identifier*)
    def e16(self):
        aux = self.nextToken()
        self.arq_saida.write(aux.lexeme)
        token = self.nextToken()
        b = True

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
```

## Exemplos

<details>

<summary>Programa 1 </summary>

### Código em Mini

```
program teste1
declare
    integer a, b, c;
    integer result;
begin
    read (a);
    read (c);
    b := 10;
    result := (a * c)/(b + 5 % 345 -3) ;
    write(result)
end
```
### Saída do programa 1 (Analisador Léxico e Sintático)

```
Recebido o token: program do Léxico
Recebido o token: teste1 do Léxico
Recebido o token: declare do Léxico
Recebido o token: integer do Léxico
Recebido o token: a do Léxico
Recebido o token: , do Léxico
Recebido o token: b do Léxico
Recebido o token: , do Léxico
Recebido o token: c do Léxico
Recebido o token: ; do Léxico
Recebido o token: integer do Léxico
Recebido o token: result do Léxico
Recebido o token: ; do Léxico
Recebido o token: begin do Léxico
Recebido o token: read do Léxico
Recebido o token: ( do Léxico
Recebido o token: a do Léxico
Recebido o token: ) do Léxico
Recebido o token: ; do Léxico
Recebido o token: read do Léxico
Recebido o token: ( do Léxico
Recebido o token: c do Léxico
Recebido o token: ) do Léxico
Recebido o token: ; do Léxico
Recebido o token: b do Léxico
Recebido o token: := do Léxico
Recebido o token: 10 do Léxico
Recebido o token: ; do Léxico
Recebido o token: result do Léxico
Recebido o token: := do Léxico
Recebido o token: ( do Léxico
Recebido o token: a do Léxico
Recebido o token: * do Léxico
Recebido o token: c do Léxico
Recebido o token: ) do Léxico
Recebido o token: / do Léxico
Recebido o token: ( do Léxico
Recebido o token: b do Léxico
Recebido o token: + do Léxico
Recebido o token: 5 do Léxico
Recebido o token: write do Léxico
ERRO! Esperado ")" recebido, write
Recebido o token: ( do Léxico
ERRO! Esperado ")" recebido, (
Recebido o token: result do Léxico
ERRO! Esperado ")" recebido, result
Recebido o token: ) do Léxico
Recebido o token: end do Léxico
ERRO! Esperado ";" recebido end
Recebido o token: FIM do Léxico
Recebido o token: FIM do Léxico
Recebido o token: FIM do Léxico
Falha na analisa sintática!
```

### Saída da Tabela de Símbolo
```
if Tag: 5
else Tag: 6
program Tag: 0
begin Tag: 1
end Tag: 2
while Tag: 12
do Tag: 11
then Tag: 8
for Tag: 13
and Tag: 39
or Tag: 38
mod Tag: 14
integer Tag: 3
decimal Tag: 4
declare Tag: 7
true Tag: 43
false Tag: 44
read Tag: 9
write Tag: 69
ID: teste1
ID: a
ID: b
ID: c
ID: result
```

</details>

<details>

<summary>Programa 2</summary>

### Código em Mini

```
program teste2
declarando
    integer a;
    integer b;
    integer c;
begin
    read (a);
    b := a * a;
    c := b + a/2 * (3 + 5);
    write(c)
end
```

### Saída do programa 2 (Analisador Léxico e Sintático)

```
Recebido o token: program do Léxico
Recebido o token: teste2 do Léxico
Recebido o token: declarando do Léxico
ERRO! Esperado a palavra "declare" ou "begin", recebido declarando
Recebido o token: integer do Léxico
ERRO! Esperado a palavra "declare" ou "begin", recebido integer
Recebido o token: a do Léxico
ERRO! Esperado a palavra "declare" ou "begin", recebido a
Recebido o token: ; do Léxico
ERRO! Esperado a palavra "declare" ou "begin", recebido ;
Recebido o token: integer do Léxico
ERRO! Esperado a palavra "declare" ou "begin", recebido integer
Recebido o token: b do Léxico
ERRO! Esperado a palavra "declare" ou "begin", recebido b
Recebido o token: ; do Léxico
ERRO! Esperado a palavra "declare" ou "begin", recebido ;
Recebido o token: integer do Léxico
ERRO! Esperado a palavra "declare" ou "begin", recebido integer
Recebido o token: c do Léxico
ERRO! Esperado a palavra "declare" ou "begin", recebido c
Recebido o token: ; do Léxico
ERRO! Esperado a palavra "declare" ou "begin", recebido ;
Recebido o token: begin do Léxico
Recebido o token: read do Léxico
Recebido o token: ( do Léxico
Recebido o token: a do Léxico
Recebido o token: ) do Léxico
Recebido o token: ; do Léxico
Recebido o token: b do Léxico
Recebido o token: := do Léxico
Recebido o token: a do Léxico
Recebido o token: * do Léxico
Recebido o token: a do Léxico
Recebido o token: ; do Léxico
Recebido o token: c do Léxico
Recebido o token: := do Léxico
Recebido o token: b do Léxico
Recebido o token: + do Léxico
Recebido o token: a do Léxico
Recebido o token: / do Léxico
Recebido o token: 2 do Léxico
Recebido o token: * do Léxico
ERRO! Esperado ";" recebido *
Recebido o token: ( do Léxico
ERRO! Esperado ";" recebido (
Recebido o token: 3 do Léxico
ERRO! Esperado ";" recebido 3
Recebido o token: + do Léxico
ERRO! Esperado ";" recebido +
Recebido o token: 5 do Léxico
ERRO! Esperado ";" recebido 5
Recebido o token: ) do Léxico
ERRO! Esperado ";" recebido )
Recebido o token: ; do Léxico
Recebido o token: write do Léxico
Recebido o token: ( do Léxico
Recebido o token: c do Léxico
Recebido o token: ) do Léxico
Recebido o token: end do Léxico
ERRO! Esperado ";" recebido end
Recebido o token: FIM do Léxico
Recebido o token: FIM do Léxico
Recebido o token: FIM do Léxico
Falha na analisa sintática!
```

### Saída da Tabela de Simbolo

```
if Tag: 5
else Tag: 6
program Tag: 0
begin Tag: 1
end Tag: 2
while Tag: 12
do Tag: 11
then Tag: 8
for Tag: 13
and Tag: 39
or Tag: 38
mod Tag: 14
integer Tag: 3
decimal Tag: 4
declare Tag: 7
true Tag: 43
false Tag: 44
read Tag: 9
write Tag: 69
ID: teste2
ID: declarando
ID: a
ID: b
ID: c
```
</details>

<details>

<summary>Programa 3</summary>

### Código em Mini

```
program teste3
declare
    integer id, qtd, cont, soma;
begin
    qtd := 5;
    cont := 5;
    soma := 0;
    do
        write("Idade: ");
        read (id);
        soma := soma # id;
        cont := cont - 1;
    while(cont > 0);
    write("Media: ");
    write (soma / qtd);
end
```

### Saída do programa 2 (Analisador Léxico e Sintático)

```
Recebido o token: program do Léxico
Recebido o token: teste3 do Léxico
Recebido o token: declare do Léxico
Recebido o token: integer do Léxico
Recebido o token: id do Léxico
Recebido o token: , do Léxico
Recebido o token: qtd do Léxico
Recebido o token: , do Léxico
Recebido o token: cont do Léxico
Recebido o token: , do Léxico
Recebido o token: soma do Léxico
Recebido o token: ; do Léxico
Recebido o token: begin do Léxico
Recebido o token: qtd do Léxico
Recebido o token: := do Léxico
Recebido o token: 5 do Léxico
Recebido o token: ; do Léxico
Recebido o token: cont do Léxico
Recebido o token: := do Léxico
Recebido o token: 5 do Léxico
Recebido o token: ; do Léxico
Recebido o token: soma do Léxico
Recebido o token: := do Léxico
Recebido o token: 0 do Léxico
Recebido o token: ; do Léxico
Recebido o token: do do Léxico
Recebido o token: write do Léxico
Recebido o token: ( do Léxico
Recebido o token: "Idade: " do Léxico
Recebido o token: ) do Léxico
Recebido o token: ; do Léxico
Recebido o token: read do Léxico
Recebido o token: ( do Léxico
Recebido o token: id do Léxico
Recebido o token: ) do Léxico
Recebido o token: ; do Léxico
Recebido o token: soma do Léxico
Recebido o token: := do Léxico
Recebido o token: soma do Léxico
Erro léxico: O token não foi reconhecido: #
Recebido o token: # do Léxico
ERRO! Esperado ";" recebido #
Recebido o token: id do Léxico
ERRO! Esperado ";" recebido id
Recebido o token: ; do Léxico
Recebido o token: cont do Léxico
Recebido o token: := do Léxico
Recebido o token: cont do Léxico
Recebido o token: - do Léxico
Recebido o token: 1 do Léxico
Recebido o token: ; do Léxico
Recebido o token: while do Léxico
Recebido o token: ( do Léxico
Recebido o token: cont do Léxico
Recebido o token: > do Léxico
Recebido o token: 0 do Léxico
Recebido o token: ) do Léxico
Recebido o token: ; do Léxico
Recebido o token: write do Léxico
Recebido o token: ( do Léxico
Recebido o token: "Media: " do Léxico
Recebido o token: ) do Léxico
Recebido o token: ; do Léxico
Recebido o token: write do Léxico
Recebido o token: ( do Léxico
Recebido o token: soma do Léxico
Recebido o token: / do Léxico
Recebido o token: qtd do Léxico
Recebido o token: ) do Léxico
Recebido o token: ; do Léxico
Recebido o token: end do Léxico
Recebido o token: FIM do Léxico
Falha na analisa sintática!
```


### Saída Tabela de Símbolo

```
if Tag: 5
else Tag: 6
program Tag: 0
begin Tag: 1
end Tag: 2
while Tag: 12
do Tag: 11
then Tag: 8
for Tag: 13
and Tag: 39
or Tag: 38
mod Tag: 14
integer Tag: 3
decimal Tag: 4
declare Tag: 7
true Tag: 43
false Tag: 44
read Tag: 9
write Tag: 69
ID: teste3
ID: id
ID: qtd
ID: cont
ID: soma
```


</details>








