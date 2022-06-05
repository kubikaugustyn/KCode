#  -*- coding: utf-8 -*-
__author__ = "kubik.augustyn@post.cz"

import argparse
from file import *

parser = argparse.ArgumentParser()
parser.add_argument("file_path", help="A KCode file path")
file_path = parser.parse_args().file_path
print("File path:", file_path)
mainFile = File(file_path)
files = [mainFile]

divider = "=================================================="
compileDivider = "--------------------------------------------------"
verboseCompile = True
checkForChanges = False

isFirst = True

while True:
    hasChanged = False
    for file in files:
        if mainFile.checkChange() or isFirst:
            if not hasChanged:
                print(divider)
            hasChanged = True
            print(f"{file.path} changed.")
            if file.fileExtension == ".kc":
                print(compileDivider)
                file.compile(verboseCompile)
                print(compileDivider)

    if hasChanged:
        print(divider)
    if isFirst:
        isFirst = False
        if not checkForChanges:
            break
