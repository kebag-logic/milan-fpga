#!/usr/bin/env python3
"""Compare inventory_learn.py lists of a base and of heads: the entries each head needs that its base does not
(what the change itself leaves unrecorded) and the reverse, one line per entry.

usage: python3 inventory_compare.py <base-label>=<base.jsonl> <head-label>=<head.jsonl> [...]
"""
import json
import sys


def load(path):
    return set(open(path).read().splitlines())


def show(line):
    entry = json.loads(line)
    if 'pattern' in entry:
        words = entry['pattern']
        out = words[words.index('-o') + 1] if '-o' in words else ' '.join(words[:3])
        return f"{entry['command']} argument pattern ({len(words)} words, output {out}) at {entry['at']}"
    if 'executable' in entry:
        return f"{entry['command']} executable {entry['executable']}"
    kind = 'repin' if 'repin' in entry else 'declare'
    return f"script {entry['script']} {kind} {entry[kind]}"


(base_label, base_path), *heads = [arg.split('=', 1) for arg in sys.argv[1:]]
base = load(base_path)
print(f'{base_label}: {len(base)} entries its own committed table lacks')
for line in sorted(base):
    print('  ' + show(line))
for label, path in heads:
    head = load(path)
    print(f'\n{label} needs, {base_label} does not: {len(head - base)}')
    for line in sorted(head - base):
        print('  + ' + show(line))
    print(f'{base_label} needs, {label} does not: {len(base - head)}')
    for line in sorted(base - head):
        print('  - ' + show(line))
