#!/usr/bin/env python
from __future__ import print_function

import sys
from random import randrange as rr
if __package__ is None or __package__ == '':
    from os.path import basename
    from classes.Utils import *
    from classes.Compiler import *
else:
    from os.path import basename
    from .classes.Utils import *
    from .classes.Compiler import *


FILL_WITH_RANDOM_TEXT = True
TEXT_PLACE_HOLDER = "[]"

dsl_path = "./Assets/web-dsl-mapping.json"

def render_content_with_text(key, value):
    if FILL_WITH_RANDOM_TEXT:
        if key.find("card-header") != -1:
            value = value.replace(TEXT_PLACE_HOLDER, Utils.get_random_text(length_text=rr(12, 16), space_number=rr(0, 2)))
        elif key.find("list-group-item") != -1:
            value = value.replace(TEXT_PLACE_HOLDER, Utils.get_random_text(length_text=rr(18, 26), space_number=rr(0, 3)))
        elif key.find("large-title") != -1:
            value = value.replace(TEXT_PLACE_HOLDER, Utils.get_random_text(length_text=rr(11, 12), space_number=rr(0, 2)))
        elif key.find("link") != -1:
            value = value.replace(TEXT_PLACE_HOLDER, Utils.get_random_text(length_text=rr(5, 13), space_number=0))
        elif key.find("button") != -1:
            value = value.replace(TEXT_PLACE_HOLDER, Utils.get_random_text(length_text=rr(6, 9), space_number=0))
        elif key.find("footer") != -1:
            value = value.replace(TEXT_PLACE_HOLDER,
                                  Utils.get_random_text(length_text=rr(32, 38), space_number=rr(1, 4), with_upper_case=False))
        elif key.find("text") != -1:
            value = value.replace(TEXT_PLACE_HOLDER,
                                  Utils.get_random_text(length_text=rr(25, 35), space_number=rr(4, 8), with_upper_case=False))
    return value

def compileDSL(input_file):
    
    compiler = Compiler(dsl_path)

    file_uid = basename(input_file)[:basename(input_file).find(".")]
    path = input_file[:input_file.find(file_uid)]
    
    input_file_path = "{}{}.dsl".format(path, file_uid)
    output_file_path = "{}{}.html".format(path, file_uid)
    
    compiler.compile(input_file_path, output_file_path, rendering_function=render_content_with_text)

if __name__ == "__main__":
    argv = sys.argv[1:]
    length = len(argv)
    if length != 0:
        input_file = argv[0]
        compileDSL(input_file)
    else:
        print("Error: not enough argument supplied:")
        print("web-compiler.py <path> <file name>")
        exit(0)