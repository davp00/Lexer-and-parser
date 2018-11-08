import re


class Parser:

    regex = '(<[a-zA-Z]+>)'

    def __init__(self, lexer):
        self.rules = {}
        self.lexer = lexer
        self.last_key = ""
        self.last_component = []
        self.c_analyzed = 0

    def add_rule(self, key='', components=''):
        self.rules[key] = components
        return self.rules[key]

    def syntax(self, rule_key, vec): # Siendo vec un vector con todos los tokens

        rule = self.rules.get(rule_key)

        components = rule

        while '|' in components:
            components = components.split('|')

        is_array = type(components) in (tuple, list)

        if is_array is False:
            components = [components]

        cont = 0

        for component in components:

            keys = self.get_keys(component)

            tk = vec.copy()

            for key in keys:

                self.last_component = keys

                if key in self.rules:
                    value = self.syntax(key, vec)
                    if value:
                        vec = value[1]
                    else:
                        return False
                else:
                    if self.compare(key, vec) is False:
                        # print('_________________________')
                        vec = tk
                        cont = cont + 1
                        break

        if cont >= len(components):
            return False
        else:
            return True, vec

    def parse_vec(self, rule_key, vec):

        value = self.syntax(rule_key, vec)

        if value:
            return self.last_key == self.last_component.pop(), value[1]
        else:
            return False

    def compare(self, key, vec):
        if key in self.lexer.dictionary:

            if len(vec) != 0:
                data = vec[0]
            else:
                return False

            value = self.lexer.compare(key, data)

            self.last_key = key

            # print("{} -> \'{}\' = {}".format(key, data, value))

            vec.pop(0)

            return value
        else:
            return False

    def get_keys(self, cad):
        return re.findall(self.regex, cad)

    def analyze(self, tokens):

        cont = 0
        data = None
        key = ''
        field_1 = None
        field_2 = None
        comparator = '<VarName>'
        text = ''

        for token in tokens:

            vec = tokens[cont: len(tokens)]
            cont = cont + 1

            if self.lexer.compare('<Literal>', token):
                data = vec[0:2]
                key = '<VarAssign>'

            elif self.lexer.compare('<Control>', token):
                field_1 = vec[2]
                field_2 = vec[4]
                key = '<IfCondition>'

            value = self.parse_vec(key, vec)

            if value:

                text = ''

                if key == '<VarAssign>':

                    self.lexer.new_identifier(data[1], data[0])

                elif key == '<IfCondition>':

                    if self.lexer.ids_defined(field_1, comparator) is False or\
                            self.lexer.ids_defined(field_2, comparator) is False:
                        text = '-- Identificadores no definidos'

                print('Analisis Correcto {}'.format(text))
                self.analyze(value[1])

                return True
            else:
                print('Error en la sintaxis')
                return False
            break