from components.lexer import Lexer
from components.parser import Parser

lexer = Lexer()

lexer.add(key='<Integer>', re_key='([0-9])+')
lexer.add(key='<VarName>', re_key='[a-zA-Z]([a-zA-Z]|[0-9])*')

lexer.add(key='<Control>', default=['if'])
lexer.add(key='<DataType>', default=['int', 'string', 'bool'])
lexer.add(key='<Comparator>', default=['==', '>', '<' '>=', '<='])
lexer.add(key='<Equals>', default=['='])
lexer.add(key='<EndSentence>', default=[';'])
lexer.add(key='<StartCondition>', default=['('])
lexer.add(key='<EndCondition>', default=[')'])
lexer.add(key='<StartBrace>', default=['{'])
lexer.add(key='<EndBrace>', default=['}'])

parser = Parser(lexer)

parser.add_rule(key='<Assign>', components='<VarName> <Equals> ::= <Integer> <EndSentence> | <VarName> <EndSentence>')
parser.add_rule(key='<VarAssign>', components='<DataType> <Assign>')
parser.add_rule(key='<Condition>', components='<StartCondition>  <EndCondition>')
parser.add_rule(key='<IfSentence>', components='<Control> <Condition> <StartBrace> <EndBrace>')

sentence = ['int','qlitos', '=', 'q12', ';']
if_sentence = ['if', '(', ')', '{', '}']

if parser.syntax('<IfSentence>', if_sentence):
    print("Analisis Correcto")
else:
    print("Errores en la sintaxis")