#  -*- coding: utf-8 -*-
__author__ = "kubik.augustyn@post.cz"

from copy import copy


class TokenAttributes:
    def __init__(self):
        self.TYPE = "type"
        self.CONST_VARIABLE = "const_variable"
        self.VARIABLE_TYPE = "variable_type"
        self.VARIABLE_NAME = "variable_name"


class TokenTypes:
    def __init__(self):
        self.VARIABLE = "variable"


TATTR = TokenAttributes()
TTYPE = TokenTypes()
NONE = None


class Token:
    def __init__(self):
        self.arguments = {}

    def __setitem__(self, key, value):
        self.arguments[key] = value

    def __getitem__(self, item):
        try:
            return self.arguments[item]
        except:
            return None


class Lexer:
    def __init__(self, lines):
        self.lines = lines
        self.tokens = []
        self._phrase = ""
        self._token = Token()
        self._var_types = [
            "any",
            "int",
            "str",
            "void",
            "bool",
            "arr",
            "obj"
        ]
        self._make_tokens()

    def _reset_phrase(self):
        temp = copy(self._phrase)
        self._phrase = ""
        return temp

    def _add_token(self):
        self.tokens.append(self._token)
        self._token = Token()

    def _set_token_attribute(self, key, value):
        self._token[key] = value

    def _is_token_attribute(self, key, value):
        return self._token[key] == value

    def _make_tokens(self):
        for line in self.lines:
            for char in line:
                self._phrase += char
                print(self._phrase)
                if self._phrase == "var" or self._phrase == "const":
                    self._set_token_attribute(TATTR.TYPE, TTYPE.VARIABLE)
                    self._set_token_attribute(TATTR.CONST_VARIABLE, self._phrase == "const")
                    self._reset_phrase()
                elif self._is_token_attribute(TATTR.TYPE, TTYPE.VARIABLE):
                    if self._var_types.__contains__(self._phrase):
                        self._set_token_attribute(TATTR.VARIABLE_TYPE, self._phrase)
                        self._reset_phrase()
                    elif char == " " and not self._is_token_attribute(TATTR.VARIABLE_TYPE, NONE):
                        self._set_token_attribute(TATTR.VARIABLE_NAME, self._phrase[:-1])
                        self._reset_phrase()
                    elif self._phrase == " ":
                        self._reset_phrase()
            self._reset_phrase()
            self._add_token()
