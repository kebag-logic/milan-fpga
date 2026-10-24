#!/usr/bin/env python3
"""For named Verilator builds, the differences between the command a tree's Makefile really runs (from an
inventory_learn.py list) and the command-table pattern that tree commits for the same output, so a base's
drift can be told from a change's own: equal residues mean the change adds no difference of its own.

usage: python3 pattern_residue.py <learn.jsonl> <command-table.json> <output> [<output> ...]
Prints each output's residue as difflib opcodes over the two word lists (equal runs omitted).
"""
import difflib
import json
import sys

learn, table_path, outputs = sys.argv[1], sys.argv[2], sys.argv[3:]
actual = {}
for line in open(learn):
    entry = json.loads(line)
    words = entry.get('pattern')
    if entry.get('command') == 'verilator' and words and '-o' in words:
        actual[words[words.index('-o') + 1]] = words
patterns = json.load(open(table_path))['commands']['verilator']['patterns']
for out in outputs:
    committed = [p for p in patterns if '-o' in p and p[p.index('-o') + 1] == out]
    if out not in actual:
        print(f'{out}: no unmatched command for it (none run, or the committed pattern matches)')
        continue
    if len(committed) != 1:
        print(f'{out}: {len(committed)} committed patterns')
        continue
    ops = difflib.SequenceMatcher(a=committed[0], b=actual[out], autojunk=False).get_opcodes()
    residue = [(tag, committed[0][i1:i2], actual[out][j1:j2]) for tag, i1, i2, j1, j2 in ops if tag != 'equal']
    print(f'{out}: {len(residue)} difference(s), table -> Makefile')
    for tag, old, new in residue:
        print(f'  {tag}: {old} -> {new}')
