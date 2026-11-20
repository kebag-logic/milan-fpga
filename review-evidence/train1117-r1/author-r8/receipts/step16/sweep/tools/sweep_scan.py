#!/usr/bin/env python3
"""sweep_scan.py REPO BASE HEAD: every line the train BASE..HEAD adds, in a code, test, script or data file (not
Markdown), that carries an issue-comment ID (issuecomment-N) or a review session or finding ID (R872-1-F2, A794, ...),
each printed as path:line and the line (R865-4-R1/R2). Exit 0 when the only such lines are in DATA, the files whose
text is a record or documentation data rather than a source comment or a check's message:

  scripts/register_descriptions.json     the register reference's descriptions (a generated page's source text)
  syn/ooc/pp_resource_baseline.json      the resource gate's record, written by pp_resource_gate.py record --write
  tb/verilator/nvm_capture_cpu/measurements.json  a measurement record's provenance field

and 1 otherwise."""
import re
import subprocess
import sys

repo, base, head = sys.argv[1:4]
CODE = ('*.py', '*.cpp', '*.c', '*.h', '*.hpp', '*.sv', '*.v', '*.vlt', '*.sh', '*.ld', '*.yaml', '*.yml', '*Makefile',
        '*.mk', '*.tsv', '*.csv', '*.txt', '*.json', '*.ratchet', '*.tcl', '*.xdc')
DATA = {'scripts/register_descriptions.json', 'syn/ooc/pp_resource_baseline.json',
        'tb/verilator/nvm_capture_cpu/measurements.json'}
PATTERN = re.compile(r'issuecomment-?\d+|\b[RA]\d{3}(?:-\d+)?(?:-[A-Z]\d+)?\b')
diff = subprocess.run(['git', '-C', repo, 'diff', '-U0', '--no-color', base, head, '--', *CODE], capture_output=True,
                      text=True, check=True).stdout
path, line, hits = None, 0, []
for text in diff.splitlines():
    if text.startswith('+++ '):
        path = text[6:]
        continue
    m = re.match(r'^@@ -\S+ \+(\d+)', text)
    if m:
        line = int(m.group(1))
        continue
    if text.startswith('+'):
        if PATTERN.search(text):
            hits.append((path, line, text[1:].strip()))
        line += 1
rc = 0
print(f'sweep_scan.py {base}..{head}: {len(hits)} added line(s) with an issue-comment or review ID in code-type files')
for path, line, text in hits:
    kind = 'DATA (kept)' if path in DATA else 'SOURCE'
    rc |= path not in DATA
    print(f'{kind} {path}:{line}: {text[:200]}')
print(f'RESULT: {"PASS: none in a source comment or check text" if rc == 0 else "FAIL"}')
sys.exit(rc)
