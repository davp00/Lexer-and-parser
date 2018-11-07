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
        principal = rule.split('::=')

        if len(principal) > 1:
            keys = self.get_keys(principal[0])
            for key in keys:
                compare_key = self.compare(key, vec)
                if compare_key is 1:
                    return self.syntax(key, vec)
                elif compare_key is True:
                    pass
                elif compare_key is None:
                    return False
            principal.pop(0)

        components = principal[0]

        while '|' in components:
            components = components.split('|')

        try:
            is_array = type(components) in (tuple, list)
            cont = 0
            if is_array is False:
                components = [components]

            for component in components:
                keys = self.get_keys(component)
                for key in keys:
                    compare_key = self.compare(key, vec)
                    if compare_key is 1:
                        value = self.syntax(key, vec)
                    elif compare_key:
                        pass
                    else:
                        cont = cont + 1
                        break
            if cont == len(components):
                return False
            return True
        except ValueError:
            return False

    def compare(self, key, vec):
        if key in self.lexer.dictionary:
            if len(vec) != 0:
                data = vec[0]
            else:
                return False
            value = self.lexer.compare(key, data)
            print("{} -> {} = {}".format(key, data, value))
            if value:
                vec.pop(0)
            return value
        else:
            return 1

    def get_keys(self, cad):
        return re.findall(self.regex, cad)
