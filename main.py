from components.lexer import Lexer
from components.parser import Parser

text = """
    int a = 30;
    int b = 30;
    if ( a > b )
    {
    }
"""


lexer = Lexer()

lexer.add(key='<Integer>', re_key='([0-9])+')
lexer.add(key='<VarName>', re_key='[a-zA-Z]([a-zA-Z]|[0-9])*')

lexer.add(key='<Control>', default=['if','while'])
lexer.add(key='<Literal>', default=['int', 'string', 'bool'])
lexer.add(key='<Comparator>', default=['==', '>', '<', '>=', '<='])
lexer.add(key='<Equals>', default=['='])
lexer.add(key='<EndSentence>', default=[';'])
lexer.add(key='<LPar>', default=['('])
lexer.add(key='<RPar>', default=[')'])
lexer.add(key='<LBrace>', default=['{'])
lexer.add(key='<RBrace>', default=['}'])

parser = Parser(lexer)

parser.add_rule(key='<Assign>', components='<VarName> <Equals> <EndSentence>'
                                           '|<VarName> <Equals> <Integer> <EndSentence>'
                                           '|<VarName> <Equals> <VarName> <EndSentence>')

parser.add_rule(key='<VarAssign>', components='<Literal> <Assign>')

parser.add_rule(key='<Comparable>', components='<VarName> <Comparator> <VarName>'
                                               '|<VarName> <Comparator> <Integer>'
                                               '|<Integer> <Comparator> <VarName>'
                                               '|<Integer> <Comparator> <Integer>')

parser.add_rule(key='<Condition>', components='<LPar> <Comparable> <RPar>')

parser.add_rule(key='<IfCondition>', components='<Control> <Condition> <LBrace> <RBrace>')

tokens = lexer.split(text)
parser.analyze(tokens)
