from .tokens import Token, TokenType

DIGITS = '0123456789'
SPACE = ' '
TAB = ['    ']
NEWLINE = ['\n', '\r']
STRING = ["'", '"']
ALLPARENS = "()[]{}"
DATATYPES = ['int', 'bool', 'arr', 'any', 'void', 'str', 'obj', 'char']


class Lexer:
    def __init__(self, text):
        self.text = iter(text)
        self.advance()

    def advance(self):
        try:
            self.current_char = next(self.text)
        except StopIteration:
            self.current_char = None

    def generate_tokens(self):
        while self.current_char != None:
            if self.current_char in SPACE:
                num = self.get_spaces_num()
                for t in TAB:
                    if num % len(t) == 0:
                        for _ in range(int(num / len(t))):
                            yield Token(TokenType.TAB)
            elif self.current_char == '.' or self.current_char in DIGITS:
                yield self.generate_number()
            elif self.current_char == '+':
                self.advance()
                yield Token(TokenType.PLUS)
            elif self.current_char == '-':
                self.advance()
                yield Token(TokenType.MINUS)
            elif self.current_char == '*':
                self.advance()
                yield Token(TokenType.MULTIPLY)
            elif self.current_char == '/':
                self.advance()
                yield Token(TokenType.DIVIDE)
            elif self.current_char == '(':
                self.advance()
                yield Token(TokenType.LPAREN)
            elif self.current_char == ')':
                self.advance()
                yield Token(TokenType.RPAREN)
            elif self.current_char == '[':
                self.advance()
                yield Token(TokenType.LBRACKET)
            elif self.current_char == ']':
                self.advance()
                yield Token(TokenType.RBRACKET)
            elif self.current_char == '{':
                self.advance()
                yield Token(TokenType.LBRACE)
            elif self.current_char == '}':
                self.advance()
                yield Token(TokenType.RBRACE)
            elif self.current_char in TAB:
                yield Token(TokenType.TAB)
                self.advance()
            elif self.current_char in NEWLINE:
                yield self.generate_newline()
            elif self.current_char in STRING or self.current_char == "d":
                if self.current_char == "d":
                    self.advance()
                    if self.current_char not in STRING:
                        continue
                    str_type = TokenType.DYNAMICSTRING
                else:
                    str_type = TokenType.STRING
                yield self.generate_string(str_type)
            elif self.current_char == "=":
                yield self.generate_equals()
            elif self.current_char == ":":
                yield Token(TokenType.COLON)
                self.advance()
            elif self.current_char == ",":
                yield Token(TokenType.COMMA)
                self.advance()
            elif self.current_char == "#":
                yield self.generate_comment()
            else:
                phrase = self.generate_to_space_or_token()
                comma = False
                if phrase.endswith(","):
                    comma = True
                    phrase = phrase[:-1]
                if phrase == 'import':
                    yield Token(TokenType.IMPORT)
                elif phrase == "as":
                    yield Token(TokenType.AS)
                elif phrase == "from":
                    yield Token(TokenType.FROM)
                elif phrase == "return":
                    yield Token(TokenType.RETURN)
                elif phrase == "is":
                    yield Token(TokenType.IS)
                elif phrase == "const":
                    yield Token(TokenType.CONST)
                elif phrase == "var":
                    yield Token(TokenType.VAR)
                elif phrase == "dynvar":
                    yield Token(TokenType.DYNAMICVAR)
                elif phrase in DATATYPES:
                    yield Token(TokenType.DATATYPE, phrase)
                else:
                    # raise Exception(f"Illegal character or phrase '{phrase}'")
                    yield Token(TokenType.PHRASE, phrase)
                if comma:
                    yield Token(TokenType.COMMA)

    def generate_newline(self):
        self.advance()
        if self.current_char in NEWLINE:
            self.advance()
        return Token(TokenType.NEWLINE)

    def generate_equals(self):
        num_equals = 0
        while self.current_char is not None and self.current_char == "=":
            num_equals += 1
            self.advance()
        if num_equals == 1:
            return Token(TokenType.EQUALS)
        elif num_equals == 2:
            return Token(TokenType.IS)
        else:
            raise Exception(f"Illegal number of '=': {num_equals}")

    def generate_string(self, str_type=TokenType.STRING):
        beginning = self.current_char
        text = ''
        self.advance()
        multiline = False
        if self.current_char == "*":
            self.advance()
            multiline = True

        while self.current_char is not None:
            if self.current_char == beginning and not multiline:
                self.advance()
                break
            elif self.current_char == "*" and multiline:
                self.advance()
                if self.current_char == beginning:
                    self.advance()
                    break
                else:
                    text += f'*{self.current_char}'
            else:
                text += self.current_char

            self.advance()

        return Token(str_type, text)

    def get_spaces_num(self):
        num = 0
        while self.current_char is not None and self.current_char in SPACE:
            num += 1
            self.advance()
        return num

    def generate_to_space_or_token(self):
        text = self.current_char
        self.advance()

        while self.current_char is not None and self.current_char not in SPACE and self.current_char not in NEWLINE and self.current_char not in ALLPARENS:
            text += self.current_char
            self.advance()

        self.get_spaces_num()
        return text

    def generate_comment(self):
        comment = ''
        self.advance()
        if self.current_char == "#":
            multiline = False
        elif self.current_char == "*":
            multiline = True
        else:
            raise Exception(f"Illegal '{self.current_char}' after # comment beginning")
        self.advance()

        while self.current_char is not None:
            if self.current_char in NEWLINE and not multiline:
                self.advance()
                break
            elif self.current_char == "*" and multiline:
                self.advance()
                if self.current_char == "#":
                    self.advance()
                    break
                else:
                    comment += f'*{self.current_char}'
            else:
                comment += self.current_char

            self.advance()

        return Token(TokenType.COMMENT, comment)

    def generate_number(self):
        decimal_point_count = 0
        number_str = self.current_char
        self.advance()

        while self.current_char != None and (self.current_char == '.' or self.current_char in DIGITS):
            if self.current_char == '.':
                decimal_point_count += 1
                if decimal_point_count > 1:
                    break

            number_str += self.current_char
            self.advance()

        if number_str.startswith('.'):
            number_str = '0' + number_str
        if number_str.endswith('.'):
            number_str += '0'

        value = float(number_str)
        if self.current_char == "E":  # 6.8E10 to 68000000000 (6.8 * 10^10)
            self.advance()
            to_power_of_ten = int(self.generate_number().value)
            value = value * (10 ** to_power_of_ten)

        return Token(TokenType.NUMBER, value)
