import re


class Lexer:
    patern = re.compile("[a-zA-Z]+|[0-9]+|[=]+|[;]|[<|>]|[+]+|[(|)]|[{|}]|[*-/]")

    def __init__(self):
        self.dictionary = {}
        self.tokens = []
        self.ids = {}

    def add(self, key='', re_key=None, default=None, components=None):
        re_key = '^'+re_key+'$' if re_key else None
        self.dictionary[key] = {
            'regex':  re_key,
            'default': default,
            'components': components
        }

    def compare(self, key, data):
        dictionary_key = self.dictionary.get(key)
        if dictionary_key:

            if dictionary_key.get('default'):

                val = data in dictionary_key.get('default')
                return val

            elif dictionary_key.get('regex'):
                return True if re.search(dictionary_key.get('regex'), data) else False

            else:
                print('ERROR: DATA')

        else:
            print('ERROR: KEY doesn\'t exist')

    def new_identifier(self, name, literal):
        self.ids[name] = {
            'literal': literal
        }

    def ids_defined(self, name, key):
        if self.compare(key, name):
            return True if self.ids.get(name) else False
        return True

    def split(self, text):
        tokens = []

        return self.patern.findall(text)