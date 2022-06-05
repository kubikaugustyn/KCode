#  -*- coding: utf-8 -*-
__author__ = "kubik.augustyn@post.cz"

class Lexer:
    def __init__(self, lines):
        self.lines = lines
        self.tokens = []
        self._make_tokens()

    def _make_tokens(self):
        pass
