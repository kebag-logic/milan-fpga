#!/usr/bin/env python3
"""Dump gcov's per-line execution counts and branch arcs for one source of a coverage build.

usage: arcs.py <build-dir> <source-suffix, e.g. src/adp.c> <source-file>
Each .gcda whose object name matches the source's basename is read with
`gcov --json-format --branch-probabilities`; arcs marked `throw` are dropped, as the
repository's coverage reader drops them. Output: one row per measured line.
"""
import gzip, json, subprocess, sys, tempfile
from pathlib import Path

build, suffix, source = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3])
text = source.read_text().splitlines()
base = Path(suffix).name
lines = {}
functions = {}
gcdas = sorted(p for p in build.rglob('*.gcda') if p.name.startswith(base + '.') or p.name == base.replace('.c', '.gcda'))
if not gcdas:
    raise SystemExit('no .gcda for ' + suffix)
for k, gcda in enumerate(gcdas):
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(['gcov', '--json-format', '--branch-probabilities', '-o', str(gcda.parent), str(gcda)],
                       cwd=tmp, check=True, capture_output=True)
        for doc in sorted(Path(tmp).glob('*.gcov.json.gz')):
            with gzip.open(doc, 'rt') as fh:
                data = json.load(fh)
            for entry in data['files']:
                if not entry['file'].endswith(suffix):
                    continue
                for fn in entry['functions']:
                    functions[fn['name']] = (fn['start_line'], fn['end_line'])
                per = {}
                for ln in entry['lines']:
                    c, a = per.setdefault(ln['line_number'], [0, []])
                    per[ln['line_number']][0] = c + ln['count']
                    a += [b['count'] for b in ln['branches'] if not b.get('throw', False)]
                for n, (c, a) in per.items():
                    old = lines.get(n)
                    if old is None or len(a) > len(old[1]):
                        lines[n] = [max(c, old[0]) if old else c, list(a)]
                    else:
                        old[0] = max(old[0], c)
                        if len(a) == len(old[1]):
                            old[1] = [max(x, y) for x, y in zip(a, old[1])]
print(f'# {suffix}: {len(gcdas)} gcda; measured lines {len(lines)}, executed {sum(1 for c, _ in lines.values() if c)}; '
      f'raw arcs {sum(len(a) for _, a in lines.values())}, taken {sum(1 for _, a in lines.values() for x in a if x)}')
def owner(n):
    for name, (s, e) in functions.items():
        if s <= n <= e:
            return name
    return '-'
for n in sorted(lines):
    c, a = lines[n]
    flag = 'RUN ' if c else 'ZERO'
    arcs = ' '.join('T' if x else 'u' for x in a)
    print(f'{owner(n):<22} {flag} arcs={len(a)} [{arcs}] | {text[n - 1].strip()}')
