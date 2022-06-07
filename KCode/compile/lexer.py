#  -*- coding: utf-8 -*-
__author__ = "kubik.augustyn@post.cz"

from copy import copy


class TokenAttributes:
    def __init__(self):
        self.TYPE = "type"
        self.CONST_VARIABLE = "const_variable"
        self.VARIABLE_TYPE = "variable_type"
        self.VARIABLE_TYPE_EXTEND = "variable_type_extend"
        self.VARIABLE_NAME = "variable_name"
        self.VARIABLE_VALUE_STRING = "variable_value_string"
        self.CONST_FUNCTION = "const_function"
        self.FUNCTION_RETURN_TYPE = "function_return_type"


class TokenTypes:
    def __init__(self):
        self.VARIABLE = "variable"
        self.FUNCTION = "function"


TATTR = TokenAttributes()
TTYPE = TokenTypes()
NONE = None
TAB = '    '


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
            "bool",
            "arr",
            "obj"
        ]
        self._func_return_types = copy(self._var_types)
        self._func_return_types.append("void")
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

    def _error(self, message):
        print(message)
        exit(1)

    def _is_at_start(self, arr=None, string=""):
        if arr is None:
            arr = []
        for item in arr:
            if string.find(item) == 0:
                return True, string[:len(item)], string[len(item):]
        return False, "", ""

    def _make_tokens(self):
        #Filter out blank lines, one line and multiline comments
        new_lines = []
        comment = False
        for line in self.lines:
            if line != "" and line.lstrip()[0:2] != "##" and not comment:
                if line.lstrip()[0:2] == "#*":
                    comment = True
                else:
                    new_lines.append(line)
            elif line.rstrip()[-2:] == "*#":
                comment = False
        #Parse lines one by one
        for line in new_lines:
            line_type = ""
            stage = 0
            index = 0
            # print(f"'{line}'")
            offset = line.count(TAB)
            line = line[len(offset * TAB):]
            print(offset, f"{offset * TAB}'{line}'")
            for char in line:
                # print(f"'{self._phrase}'")
                """if self._phrase == "var" or self._phrase == "const":
                    self._set_token_attribute(TATTR.TYPE, TTYPE.VARIABLE)
                    self._set_token_attribute(TATTR.CONST_VARIABLE, self._phrase == "const")
                    self._reset_phrase()
                elif self._is_token_attribute(TATTR.TYPE, TTYPE.VARIABLE):
                    if self._var_types.__contains__(self._phrase):
                        self._set_token_attribute(TATTR.VARIABLE_TYPE, self._phrase)
                        self._reset_phrase()
                    elif char == " " and not self._is_token_attribute(TATTR.VARIABLE_TYPE, NONE) and \
                            self._is_token_attribute(TATTR.VARIABLE_NAME, NONE) and self._phrase != " ":
                        self._set_token_attribute(TATTR.VARIABLE_NAME, self._phrase[:-1])
                        self._reset_phrase()
                    elif self._phrase == " ":
                        self._reset_phrase()"""
                if char == " ":
                    if stage == 0 and line_type == "":
                        if self._phrase == "var" or self._phrase == "const":
                            line_type = "var"
                            stage += 1
                            self._set_token_attribute(TATTR.TYPE, TTYPE.VARIABLE)
                            self._set_token_attribute(TATTR.CONST_VARIABLE, self._phrase == "const")
                            self._reset_phrase()
                        elif self._phrase == "var_func" or self._phrase == "const_func":
                            line_type = "function"
                            stage += 1
                            self._set_token_attribute(TATTR.TYPE, TTYPE.FUNCTION)
                            self._set_token_attribute(TATTR.CONST_FUNCTION, self._phrase == "const_func")
                            self._reset_phrase()
                    elif line_type == "var":
                        if stage == 1:
                            found, start, end = self._is_at_start(self._var_types, self._phrase)
                            print(f'"{found}" "{start}" "{end}"')
                            if found:
                                stage += 1
                                self._set_token_attribute(TATTR.VARIABLE_TYPE, start)
                                if end:
                                    self._set_token_attribute(TATTR.VARIABLE_TYPE_EXTEND, end)
                                self._reset_phrase()
                            else:
                                self._error("Invalid variable type")
                        elif stage == 2:
                            stage += 1
                            self._set_token_attribute(TATTR.VARIABLE_NAME, self._phrase)
                            self._reset_phrase()
                        elif stage == 3 and self._phrase == "=":
                            stage += 1
                            self._reset_phrase()
                            self._set_token_attribute(TATTR.VARIABLE_VALUE_STRING, line[index + 1:])
                            break
                        else:
                            self._error("Too much values for variable.")
                    elif line_type == "function":
                        if stage == 1:
                            if self._func_return_types.__contains__(self._phrase):
                                stage += 1
                                self._set_token_attribute(TATTR.FUNCTION_RETURN_TYPE, self._phrase)
                                self._reset_phrase()
                            else:
                                self._error("Invalid function return type")
                self._phrase += char
                if self._phrase == " ":
                    self._reset_phrase()
                index += 1
            self._reset_phrase()
            self._add_token()
            print("************************************")
