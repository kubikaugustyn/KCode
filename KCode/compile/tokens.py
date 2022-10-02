from enum import Enum
from dataclasses import dataclass


# https://en.wikipedia.org/wiki/Bracket
class TokenType(Enum):
    NUMBER = 0  # 9032.922
    PLUS = 1  # +
    MINUS = 2  # -
    MULTIPLY = 3  # *
    DIVIDE = 4  # /
    LPAREN = 5  # (
    RPAREN = 6  # )
    LBRACKET = 7  # [
    RBRACKET = 8  # ]
    LBRACE = 9  # {
    RBRACE = 10  # }
    COLON = 11  # :
    IMPORT = 12  # import
    FROM = 13  # from
    EXPORT = 14  # export
    CONST = 15  # const
    VAR = 16  # var
    DYNAMICVAR = 17  # dynvar (computed always when value is read)
    DATATYPE = 18  # (int|bool|arr|any|void[only for functions]|str|obj|char|H[int in hex format])
    STRING = 19  # one line "???" and '???' or multiline "*???*" and '*???*'
    DYNAMICSTRING = 20  # same as string, but with d prefix: d'{[KCODE]a is true} [STRING]is very smart' etc.
    # computed when dynvar str = d'...' by dynvar, else only string containig KCode
    IF = 21  # if ([condition]):
    ELSE = 22  # else
    ELSEIF = 23  # elseif ([condition])
    FORLOOP = 24  # for [int] of [arr[int]]
    FUNCTION = 25  # func
    RETURN = 26  # return
    AS = 27  # (export|import) helloWorld as hw
    IS = 28  # '[a] is [b]' or '[a] == [b]' Equation comparing a and b
    AND = 29  # '[a] and [b]' or '[a] && [b]' Equation comparing if a and b are true, like AND gate
    OR = 30  # '[a] and [b]' or '[a] || [b]' Equation comparing if one or more of a and b are true, like OR gate
    GTT = 31  # '[a] is gtt [b]' or '[a] is > [b]' Return true if a is greater than b, works only with ints of any kind
    LST = 32  # '[a] is lst [b]' or '[a] is < [b]' Return true if a is less than b, works only with ints of any kind
    LSTOET = 33  # '[a] is lstoet [b]' or '[a] is <= [b]'
    # Return true if a is less than or equal to b, works only with ints of any kind
    GTTOET = 34  # '[a] is gttoet [b]' or '[a] is >= [b]'
    # Return true if a is greater than or equal to b, works only with ints of any kind
    PHRASE = 35  # anything like variable name...
    COMMA = 36  # ,
    TAB = 37  # '    '
    NEWLINE = 38  # \n, \r
    EQUALS = 39  # =
    COMMENT = 40  # ##??? Inline comment, #*???*# Multiline comment


@dataclass
class Token:
    type: TokenType
    value: any = None

    def __repr__(self):
        return self.type.name + (f": '{self.value}'" if self.value is not None else "")
