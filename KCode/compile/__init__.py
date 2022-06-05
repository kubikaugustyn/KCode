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
        lexer = Lexer(self.file.lines)
        self.print("Tokens:", lexer.tokens)
