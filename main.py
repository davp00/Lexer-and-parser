from components.lexer import Lexer
from components.parser import Parser

lexer = Lexer()

lexer.add(key='<Integer>', re_key='([0-9])+')
lexer.add(key='<VarName>', re_key='[a-zA-Z]([a-zA-Z]|[0-9])*')

lexer.add(key='<Control>', default=['if'])
lexer.add(key='<DataType>', default=['int', 'string', 'bool'])
lexer.add(key='<Equals>', default=['='])
lexer.add(key='<EndSentence>', default=';')

parser = Parser(lexer)

parser.add_rule(key='<Assign>', components='<VarName> <Equals> ::= <Integer> <EndSentence> | <VarName> <EndSentence>')
parser.add_rule(key='<VarAssign>', components='<DataType> <Assign>')

sentence = ['int','qlitos', '=', 'q12', ';']


if parser.syntax('<VarAssign>', sentence):
    print("Analisis Correcto")
else:
    print("Errores en la sintaxis")