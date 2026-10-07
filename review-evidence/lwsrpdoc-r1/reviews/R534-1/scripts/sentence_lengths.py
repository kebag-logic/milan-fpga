#!/usr/bin/env python3
"""Reviewer-owned sentence-length check, independent of doc/tools: strips fences, HTML comments and
link targets, treats each table cell, list item and heading as its own unit, joins wrapped paragraph
lines, splits on . ! ? followed by whitespace. Prints the distribution and anything over 25 words.
Usage: sentence_lengths.py <file>..."""
import re, sys, collections
LINK = re.compile(r"\[([^\]\n]+)\]\([^)\s]+\)")
dist = collections.Counter(); over = []; total = 0
for f in sys.argv[1:]:
    units = []; para = []; inf = False
    for n, l in enumerate(open(f).read().splitlines(), 1):
        if re.match(r'^\s*(~~~|```)', l):
            inf = not inf
            if para: units.append((pn, ' '.join(para))); para = []
            continue
        if inf or l.startswith('<!--'): continue
        if not l.strip():
            if para: units.append((pn, ' '.join(para))); para = []
            continue
        if l.lstrip().startswith('|'):
            if para: units.append((pn, ' '.join(para))); para = []
            units += [(n, c) for c in l.strip().strip('|').split('|') if not re.fullmatch(r'[\s:-]*', c)]
        elif re.match(r'^\s*(#+\s|[-*+]\s|\d+\.\s)', l):
            if para: units.append((pn, ' '.join(para))); para = []
            units.append((n, re.sub(r'^\s*(#+|[-*+]|\d+\.)\s+', '', l)))
        else:
            if not para: pn = n
            para.append(l.strip())
    if para: units.append((pn, ' '.join(para)))
    for n, u in units:
        u = LINK.sub(r'\1', u).replace('`', '')
        for s in re.split(r'(?<=[.!?])\s+', u):
            w = len(s.split())
            if not w: continue
            total += 1; dist[min(w // 5 * 5, 25)] += 1
            if w > 25: over.append(f'{f}:{n}: {w}: {s}')
print(f'units={total}', ' '.join(f'{k}-{k+4}:{v}' if k < 25 else f'25+:{v}' for k, v in sorted(dist.items())))
print('\n'.join(over) or 'none over 25 words')
