#!/usr/bin/env python3
"""Ask check_cpp_idiom's own reader about the suite Makefile at base and head.
usage: cpp_idiom_probe.py <repo with scripts/> <base Makefile> <head Makefile>"""
import sys
sys.path.insert(0, sys.argv[1] + "/scripts")
import check_cpp_idiom as g
print("makefiles_without_warnings at this tree:", g.makefiles_without_warnings())
for label, path in (("base", sys.argv[2]), ("head", sys.argv[3])):
    print(label, g.cflags_missing(open(path, encoding="utf-8").read()))
