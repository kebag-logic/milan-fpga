#!/usr/bin/env python3
"""Compare a Python file's parsed program and a text file's word sequence across two commits.

Usage: soc_program_compare.py <clone> <base> <head>
"""
import ast
import subprocess
import sys

clone, base, head = sys.argv[1:4]


def show(rev, path):
    return subprocess.run(["git", "-C", clone, "show", f"{rev}:{path}"], check=True,
                          capture_output=True, text=True).stdout


soc_a, soc_b = (show(rev, "sw/litex/milan_soc.py") for rev in (base, head))
same = ast.dump(ast.parse(soc_a)) == ast.dump(ast.parse(soc_b))
print("milan_soc.py parsed program identical:", same, "bytes differ:", soc_a != soc_b)
doc_a, doc_b = (show(rev, "tb/verilator/gptp_txts/README.md") for rev in (base, head))
words = doc_a.split() == doc_b.split()
print("gptp_txts/README.md word sequence identical:", words, "bytes differ:", doc_a != doc_b)
sys.exit(0 if same and words else 1)
