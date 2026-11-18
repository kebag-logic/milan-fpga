#!/usr/bin/env python3
"""Print each diff3 conflict hunk of a file with the candidate resolution's text for the same region.

usage: hunks.py <diff3-file> <resolved-file> [width]
The region in the resolved file is found between the hunk's preceding and following common lines
(up to 3 of each, matched in order)."""
import sys


def parse(lines):
    out, i, common = [], 0, []
    while i < len(lines):
        if lines[i].startswith('<<<<<<< '):
            ours, base, theirs, part = [], [], [], 'o'
            i += 1
            while not lines[i].startswith('>>>>>>> '):
                l = lines[i]
                if l.startswith('||||||| '):
                    part = 'b'
                elif l.startswith('=======') and l.rstrip('\n') == '=======':
                    part = 't'
                else:
                    {'o': ours, 'b': base, 't': theirs}[part].append(l)
                i += 1
            out.append(('H', ours, base, theirs))
        else:
            out.append(('C', lines[i]))
        i += 1
    return out


def main():
    d3 = open(sys.argv[1]).read().splitlines(True)
    res = open(sys.argv[2]).read().splitlines(True)
    w = int(sys.argv[3]) if len(sys.argv) > 3 else 200
    items = parse(d3)
    # map common lines in order onto the resolved file
    pos = 0
    n = 0
    for k, it in enumerate(items):
        if it[0] == 'C':
            continue
        n += 1
        before = [x[1] for x in items[max(0, k - 3):k] if x[0] == 'C']
        after = []
        for x in items[k + 1:]:
            if x[0] != 'C':
                break
            after.append(x[1])
            if len(after) == 3:
                break
        # find 'before' block in res from pos
        start = pos
        if before:
            for j in range(pos, len(res) - len(before) + 1):
                if res[j:j + len(before)] == before:
                    start = j + len(before)
                    break
            else:
                start = None
        end = None
        if start is not None:
            if after:
                for j in range(start, len(res) - len(after) + 1):
                    if res[j:j + len(after)] == after:
                        end = j
                        break
            else:
                end = len(res)
        _, ours, base, theirs = it
        print(f'================ hunk {n}')
        for name, body in (('OURS', ours), ('BASE', base), ('THEIRS', theirs)):
            print(f'--- {name} ({len(body)} lines)')
            for l in body:
                print('  ' + l.rstrip('\n')[:w])
        if start is None or end is None:
            print('--- RESOLVED: region not located')
        else:
            print(f'--- RESOLVED ({end - start} lines, res lines {start + 1}-{end})')
            for l in res[start:end]:
                print('  ' + l.rstrip('\n')[:w])
            pos = end


main()
