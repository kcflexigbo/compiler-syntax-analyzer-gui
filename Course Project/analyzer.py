import pandas as pd

# from slrgenerator import Grammar
INTEGER = 'INTEGER'
IDENTIFIER = 'ID'
EOF = 'EOF'
KEYWORD = "keyword"
SYMBOL = 'SYMBOL'

S_PRIME = 'S\''
S = "S"
EXPR = 'EXPR'
TERM = 'TERM'
FACTOR = 'FACTOR'

# keyword_list = ["or", "and", "not", "true", "false"]
# symbol_list = ["(", ")", ";", "+", "-", "/", "*", "="]
output_table = pd.DataFrame(columns=["Current Stack", "Current Input Token", "Current Action"])


class production:
    def __init__(self, pr_head, pr_body=None, nitems=None):
        self.head = pr_head
        self.body = pr_body
        if self.body is not None:
            self.nitems = len(self.body)

    def __str__(self):
        new_str = ""
        # print(repr(self))
        for i in self.body:
            new_str += " " + repr(i)
        return f"{self.head}-> {new_str}"

    def __int__(self):
        return int(self.nitems)

    def __repr__(self):
        return str(self.head)

    def checkcontains(self, term: str) -> int | None:
        try:
            return [repr(x) for x in self.body].index(term)
        except:
            return None


class Terminal:
    def __init__(self, term):
        assert isinstance(term, str)
        self.term = term

    def __str__(self):
        return str(self.term)

    def __repr__(self):
        return str(self.term)


class Closure:
    def __init__(self, prod: production, dotPos: int):
        self.prod = prod
        self.dotPos = dotPos

    def __str__(self):
        newstr = ""
        for i in range(self.dotPos):
            newstr += repr(self.prod.body[i])
        newstr += "."
        for i in range(self.dotPos, len(self.prod.body)):
            newstr += repr(self.prod.body[i])

        return f"{self.prod.head}->{newstr}"

    def __repr__(self):
        newstr = ""
        for i in range(self.dotPos):
            newstr += repr(self.prod.body[i])
        newstr += "."
        for i in range(self.dotPos, len(self.prod.body)):
            newstr += repr(self.prod.body[i])

        return f"{self.prod.head}->{newstr}"

    def getcurrent(self):
        if self.dotPos == self.prod.nitems:
            return "END"
        return repr(self.prod.body[self.dotPos])

    def getcurrentclass(self):
        if self.dotPos == self.prod.nitems:
            return "END"
        return self.prod.body[self.dotPos]

    def getprevious(self):
        assert self.dotPos > 0
        return repr(self.prod.body[self.dotPos - 1])


class action:
    def __init__(self, type=None, new_state=None):
        self.type = type
        self.new_state = new_state

    def __str__(self):
        return str(f"{self.type}, {self.new_state}")

    def __int__(self):
        return self.new_state

    def __repr__(self):
        return str(self.type)


class follow_helper:
    def __init__(self, prod: production, termpos: int):
        self.prod = prod
        self.pos = termpos

    def __str__(self):
        return f"({str(self.prod)}, {self.pos})"
        # return repr(self.prod.body[self.pos])

    def __repr__(self):
        # return f"({str(self.prod)}, {self.pos})"
        return repr(self.prod.body[self.pos])

    def getafter(self):
        if self.pos == len(self.prod.body) - 1:
            return "LAST"
        else:
            return self.prod.body[self.pos + 1]


class Token:
    def __init__(self, in_type, value, grammar=None, symbol_table=None):
        self.type = in_type
        self.value = value
        self.table_pos = 0
        self.symbol_Table = symbol_table
        self.grammar = grammar
        self.classify_key()


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
        if self.type == INTEGER:
            return INTEGER
        elif self.type == IDENTIFIER:
            return IDENTIFIER
        else:
            return str(self.value)

    def classify_value(self):
        if self.value in self.grammar.keywordList:
            return "keyword"
        elif self.value in self.grammar.symbolList:
            return "symbol"
        return None

    def classify_key(self):
        if self.type == IDENTIFIER and self.value in self.grammar.keywordList:
            self.type = KEYWORD


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

    def skip_whitespace(self, grammar):
        cond = self.current_char in grammar.symbolList
        while self.current_char is not None and (self.current_char.isspace() or self.current_char == "\n") and not cond:
            self.advance()
            cond = self.current_char in grammar.symbolList

    def integer(self, grammar):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        if self.current_char is not None and self.current_char.isalpha():
            self.current_char = result + self.current_char
            # self.error()
            return "error"
        if not grammar.enable_integers:
            self.error(2, result)
        return int(result)

    def string(self, grammar):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        if self.current_char in grammar.symbolList:
            self.flag = True
        if not grammar.enable_identifiers:
            if result not in grammar.keywordList:
                self.error(2, result)
        return result

    def get_next_token(self, symbol_Table, grammar):
        while self.current_char is not None:
            if self.current_char.isspace() or self.current_char == "\n":
                self.skip_whitespace(grammar)
                continue

            if self.current_char.isdigit():
                temp_ret = self.integer(grammar)
                if temp_ret != "error":
                    return Token(INTEGER, temp_ret, grammar, symbol_Table)

            if self.current_char.isalpha():
                return Token(IDENTIFIER, self.string(grammar), grammar, symbol_Table)

            if self.current_char in grammar.symbolList:
                temp_ret = self.current_char
                self.advance()
                return Token(SYMBOL, temp_ret, grammar)

            self.error()
            break

        return Token(EOF, None, grammar)


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
                display_string += str(i.value)
            elif isinstance(i, states):
                display_string += str(int(i))
            elif isinstance(i, production):
                display_string += repr(i)
        return display_string

    def original_stack(self):
        self.parsing_stack = [Token(SYMBOL, "#"), states(0)]
        self.parsing_stack_length = 2

    def clear(self):
        self.parsing_stack = []
        self.parsing_stack_length = 0


class states:
    def __init__(self, state_value):
        self.state = state_value

    def __str__(self):
        return str(self.state)

    def __int__(self):
        return int(self.state)


hash_token = Token(SYMBOL, "#")

if __name__ == "__main__":
    s = production(S)
    expr = production(EXPR)
    term = production(TERM)
    factor = production(FACTOR)

    or_token = Token(IDENTIFIER, "or")
    and_token = Token(IDENTIFIER, "and")
    not_token = Token(IDENTIFIER, "not")
    true_token = Token(IDENTIFIER, "true")
    false_token = Token(IDENTIFIER, "false")
    lparen_token = Token(IDENTIFIER, "(")
    rparen_token = Token(IDENTIFIER, ")")
    semicolon_token = Token(IDENTIFIER, ";")
    hash_token = Token(SYMBOL, "#")

    s_prime_prod = production(S_PRIME, [s])
    s_prod = production(S, [expr, semicolon_token])
    expr_1_prod = production(EXPR, [expr, or_token, term])
    expr_2_prod = production(EXPR, [term])
    term_1_prod = production(TERM, [term, and_token, factor])
    term_2_prod = production(TERM, [factor])
    factor_1_prod = production(FACTOR, [not_token, factor])
    factor_2_prod = production(FACTOR, [lparen_token, expr, rparen_token])
    factor_3_prod = production(FACTOR, [true_token])
    factor_4_prod = production(FACTOR, [false_token])

    print(expr_1_prod.checkcontains("S"))
