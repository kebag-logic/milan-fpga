#!/usr/bin/env python3
"""Search every figure source and render of the repository for removed names.

Usage: figure_label_search.py REPO_ROOT
Covers: draw.io sources (every cell label, edges with source -> target),
committed SVG renders (visible text, the draw.io model attribute excluded),
WaveDrom renders, and every fenced mermaid/wavedrom block in Markdown.
Prints every label of the draw.io sources, then every hit of PATTERN.
"""
import glob
import html
import os
import re
import sys

PATTERN = re.compile(
    r'counter|adapter|READ_AS_PATH|AS_CAPABLE_CHANGE|PATH_CHANGE|INPUT_CONFIGURE|'
    r'INPUT_ENABLE|INPUT_DISABLE|INPUT_START|INPUT_STOP|SET_INPUT_FORMAT|'
    r'SET_OUTPUT_FORMAT|OUTPUT_SET_PT_OFFSET|OUTPUT_STATUS|SET_CLOCK_SOURCE|'
    r'GET_MCR_DEFAULTS|MC_LOCKED|MC_UNLOCKED|gm_changed|GM_CHANGED|tick|'
    r'B/C/D|\bbanks?\b|mask ROM', re.I)

root = sys.argv[1]
os.chdir(root)
print('## draw.io labels (id | label | edge source -> target)')
for f in sorted(glob.glob('docs/diagrams/src/*.drawio')):
    print('==', f)
    s = open(f).read()
    for m in re.finditer(r'<mxCell id="([^"]*)"(?: value="([^"]*)")?([^>]*)>', s):
        v = html.unescape(m.group(2) or '').replace('\n', ' / ')
        src = re.search(r'source="([^"]*)"', m.group(3))
        tgt = re.search(r'target="([^"]*)"', m.group(3))
        if v or src:
            print(f"  {m.group(1)} | {v} | {src.group(1) if src else ''} -> {tgt.group(1) if tgt else ''}")
print('## hits of the removed-name pattern')
for f in sorted(glob.glob('docs/diagrams/src/*.drawio')):
    for v in re.findall(r'value="([^"]*)"', open(f).read()):
        v = html.unescape(v).replace('\n', ' / ')
        if PATTERN.search(v):
            print(f'drawio {f}: {v}')
for f in sorted(glob.glob('docs/diagrams/*.svg') + glob.glob('docs/diagrams/wavedrom/*.svg')):
    s = re.sub(r'content="[^"]*"', '', open(f).read())
    lines = [html.unescape(x).strip() for x in re.sub(r'<[^>]+>', '\n', s).split('\n')]
    for x in dict.fromkeys(x for x in lines if x and PATTERN.search(x)):
        print(f'svg {f}: {x[:220]}')
for f in sorted(glob.glob('**/*.md', recursive=True)):
    text = open(f).read()
    for m in re.finditer(r'^```(mermaid|wavedrom)\n(.*?)^```', text, re.M | re.S):
        line0 = text[:m.start()].count('\n') + 1
        for i, x in enumerate(m.group(2).split('\n')):
            if PATTERN.search(x):
                print(f'{m.group(1)} {f}:{line0 + 1 + i}: {x.strip()[:220]}')
