import re

# Token types
INTEGER = 'INTEGER'
IDENTIFIER = 'ID'
EOF = 'EOF'
SYMBOL = 'SYMBOL'

keyword_list = ["int", "main", "not", "or", "and", "for", "while", "else", "if", "True", "False", "None", "NULL",
                "do", "class", "float", "double", "bool", "cout", "break", "continue", "def", "endl", "print", "cin",
                "void", "using", "namespace", "std", "include", "iostream"]
symbol_list = [",", ":", ";", "\"", "/", "+", "=", "-", "!", "@", "#", "&", "^", ".", "{", "}", "[", "]", "!",
               "(", ")", "\\", "<", ">", "?", "~", "*"]


# Token class
class Token:
    def __init__(self, type, value, symbol_table=None):
        self.type = type
        self.value = value
        self.table_pos = 0
        self.symbol_Table = symbol_table

    def __str__(self):
        classified = self.classify_value()
        if classified is not None:
            return f'<{repr(self.value)}>'
        if self.type == INTEGER:
            self.table_pos = self.symbol_Table.find_in_constant_table(self.value)
            if self.table_pos == -1:
                self.table_pos = self.symbol_Table.add_to_constant_table(self.value)
        else:
            self.table_pos = self.symbol_Table.find_in_variable_table(self.value)
            if self.table_pos == -1:
                self.table_pos = self.symbol_Table.add_to_variable_table(self.value)
        return f'<{self.type}, {repr(self.table_pos)}>'

    def __repr__(self):
        return self.__str__()

    def classify_value(self):
        if self.value in keyword_list:
            return "keyword"
        elif self.value in symbol_list:
            return "symbol"
        return None

class SymbolTables:
    def __init__(self):
        self.variable_table = []
        self.constant_table = []
        self.variable_table_length = 0
        self.constant_table_length = 0

    def add_to_variable_table(self, value):
        self.variable_table.append([self.variable_table_length + 1, value])
        self.variable_table_length += 1
        return self.variable_table_length

    def add_to_constant_table(self, value):
        self.constant_table.append([self.constant_table_length + 1, value])
        self.constant_table_length += 1
        return self.constant_table_length

    def find_in_constant_table(self, value):
        for i in self.constant_table:
            if i[1] == value:
                return i[0]
        return -1

    def find_in_variable_table(self, value):
        for i in self.variable_table:
            if i[1] == value:
                return i[0]
        return -1



# Lexer class
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.flag = False

    def error(self, type=1):
        if type == 1:
            raise Exception(f'Invalid character {self.current_char}')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def retract(self):
        self.pos -= 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        cond = self.current_char in symbol_list
        while self.current_char is not None and (self.current_char.isspace() or self.current_char == "\n") and not cond:
            self.advance()
            cond = self.current_char in symbol_list

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        if self.current_char is not None and self.current_char.isalpha():
            self.current_char = result + self.current_char
            # self.error()
            return "error"
        return int(result)

    def string(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        if self.current_char in symbol_list:
            self.flag = True
        return result

    def get_next_token(self, symbol_Table):
        while self.current_char is not None:
            if self.current_char.isspace() or self.current_char == "\n":
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                temp_ret = self.integer()
                if temp_ret != "error":
                    return Token(INTEGER, temp_ret, symbol_Table)

            if self.current_char.isalpha():
                return Token(IDENTIFIER, self.string(), symbol_Table)

            if self.current_char in symbol_list:
                temp_ret = self.current_char
                self.advance()
                return Token(SYMBOL, temp_ret)

            self.error()
            break

        return Token(EOF, None)
