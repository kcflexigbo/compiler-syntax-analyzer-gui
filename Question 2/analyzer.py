import re
import pandas as pd
from createParsingTables import *

# Token types
INTEGER = 'INTEGER'
IDENTIFIER = 'ID'
EOF = 'EOF'
SYMBOL = 'SYMBOL'

S_PRIME = 'S\''
S = "S"
EXPR = 'EXPR'
TERM = 'TERM'
FACTOR = 'FACTOR'

keyword_list = ["or", "and", "not", "true", "false"]
symbol_list = ["(", ")", ";"]

action_parsing_table = action_parsing_table
goto_parsing_table = goto_parsing_table

output_table = pd.DataFrame(columns=["Current Stack", "Current Input Token", "Current Action"])


# Token class
class Token:
    def __init__(self, in_type, value, symbol_table=None):
        self.type = in_type
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
        return str(self.value)

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

    def error(self, type=1, errvalue=None):
        if type == 1:
            raise Exception(f'Invalid character {self.current_char}')
        else:
            raise Exception(f'Invalid character {errvalue}')

    def advance(self):
        self.pos += 1
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
        self.error(2, result)
        return int(result)

    def string(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        if self.current_char in symbol_list:
            self.flag = True
        if result not in keyword_list:
            self.error(2, result)
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


class states:
    def __init__(self, state_value):
        self.state = state_value

    def __str__(self):
        return str(self.state)

    def __int__(self):
        return int(self.state)


class parsing_stack:
    def __init__(self):
        self.parsing_stack = [Token(SYMBOL, "#"), states(0)]
        self.parsing_stack_length = 2

    def push(self, token):
        self.parsing_stack.append(token)
        self.parsing_stack_length += 1

    def pop(self, number_of_times=0):
        if self.parsing_stack_length == 0:
            return None
        if number_of_times == 0:
            self.parsing_stack_length -= 1
            return self.parsing_stack.pop()
        else:
            n_times = number_of_times * 2
            last_object = None
            for i in range(n_times):
                self.parsing_stack_length -= 1
                last_object = self.parsing_stack.pop()
            return last_object

    def peek(self):
        if self.parsing_stack_length == 0:
            return None
        return self.parsing_stack[-1]

    def get_all(self):
        display_string = ""
        if self.parsing_stack_length == 0:
            return display_string
        for i in self.parsing_stack:
            if isinstance(i, Token):
                display_string += i.value
            elif isinstance(i, states):
                display_string += str(int(i))
            elif isinstance(i, productions):
                display_string += repr(i)
        return display_string

    def original_stack(self):
        self.parsing_stack = [Token(SYMBOL, "#"), states(0)]
        self.parsing_stack_length = 2

    def clear(self):
        self.parsing_stack = []
        self.parsing_stack_length = 0


class productions:
    def __init__(self, pr_head, pr_body=None, nitems=None):
        self.head = pr_head
        self.body = pr_body
        if self.body is not None:
            self.nitems = len(self.body)

    def __str__(self):
        new_str = ""
        for i in self.body:
            new_str += repr(i)
        return f"{self.head}-> {new_str}"

    def __int__(self):
        return int(self.nitems)

    def __repr__(self):
        return self.head


s = productions(S)
expr = productions(EXPR)
term = productions(TERM)
factor = productions(FACTOR)

or_token = Token(IDENTIFIER, "or")
and_token = Token(IDENTIFIER, "and")
not_token = Token(IDENTIFIER, "not")
true_token = Token(IDENTIFIER, "true")
false_token = Token(IDENTIFIER, "false")
lparen_token = Token(IDENTIFIER, "(")
rparen_token = Token(IDENTIFIER, ")")
semicolon_token = Token(IDENTIFIER, ";")
hash_token = Token(SYMBOL, "#")

s_prime_prod = productions(S_PRIME, [s])
s_prod = productions(S, [expr, semicolon_token])
expr_1_prod = productions(EXPR, [expr, or_token, term])
expr_2_prod = productions(EXPR, [term])
term_1_prod = productions(TERM, [term, and_token, factor])
term_2_prod = productions(TERM, [factor])
factor_1_prod = productions(FACTOR, [not_token, factor])
factor_2_prod = productions(FACTOR, [lparen_token, expr, rparen_token])
factor_3_prod = productions(FACTOR, [true_token])
factor_4_prod = productions(FACTOR, [false_token])

production_Lists = [s_prime_prod,
                    s_prod,
                    expr_1_prod,
                    expr_2_prod,
                    term_1_prod,
                    term_2_prod,
                    factor_1_prod,
                    factor_2_prod,
                    factor_3_prod,
                    factor_4_prod]

if __name__ == "__main__":
    pass
    # for i in production_Lists:
    #     print(str(i))
    # new_row = [1, 2, 3, 4]
    # for i in range(4):
    #     output_table.loc[len(output_table.index)] = new_row
    # print(output_table)
    #
    # output_table.drop(output_table.index, inplace=True)
    # print(output_table)
