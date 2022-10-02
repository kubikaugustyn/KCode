#  -*- coding: utf-8 -*-
__author__ = "kubik.augustyn@post.cz"

import os
import compile


class File:
    def __init__(self, path, cached_stamp=None):
        self.path = path
        self.dir, self.file = os.path.split(self.path)
        self.fileName, self.fileExtension = os.path.splitext(self.file)
        self._cached_stamp = cached_stamp
        if self._cached_stamp is None:
            self._cached_stamp = os.stat(path).st_mtime
        with open(self.path, "r") as f:
            self.content = f.read()
            self.lines = self.content.splitlines()
            self.content_lines = "\n".join(self.lines)
        self.compiler = compile.Compiler(self)

    def checkChange(self):
        stamp = os.stat(self.path).st_mtime
        content = None
        if stamp != self._cached_stamp:
            self._cached_stamp = stamp
            content = self.content
            self.__init__(self.path, self._cached_stamp)
            if content != self.content:
                # File has changed, so do something..
                # print(f"File {self.file} has changed!")
                # print(self.content_lines)
                return True
        return False

    def compile(self, verboseCompile=False):
        self.compiler.compile(verboseCompile)
