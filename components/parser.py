import re


class Parser:

    regex = '(<[a-zA-Z]+>)'

    def __init__(self, lexer):
        self.rules = {}
        self.lexer = lexer

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
                if key in self.rules:
                    value = self.syntax(key, vec)
                    if value:
                        vec = value[1]
                else:
                    if self.compare(key, vec) is False:
                        print('_________________________')
                        vec = tk
                        cont = cont + 1
                        break

        if cont >= len(components):
            return False
        else:
             return True, vec

    def compare(self, key, vec):
        if key in self.lexer.dictionary:
            if len(vec) != 0:
                data = vec[0]
            else:
                return False
            value = self.lexer.compare(key, data)
            print("{} -> \'{}\' = {}".format(key, data, value))
            vec.pop(0)
            return value
        else:
            return False

    def get_keys(self, cad):
        return re.findall(self.regex, cad)
