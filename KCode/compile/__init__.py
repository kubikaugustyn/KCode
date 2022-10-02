#  -*- coding: utf-8 -*-
__author__ = "kubik.augustyn@post.cz"

from .lexer import Lexer


class Compiler:
    def __init__(self, file):
        self.file = file
        self.verboseCompile = False

    def print(self, *args, sep=' ', end='\n', file=None):
        if self.verboseCompile:
            print(*args, sep=sep, end=end, file=file)

    def compile(self, verboseCompile):
        self.verboseCompile = verboseCompile
        self.print("Compile", self.file.path)
        lexer = Lexer(self.file.content)
        tokens = lexer.generate_tokens()
        self.print("Tokens:", tokens)
        for token in tokens:
            print(f"Token: {token}")
