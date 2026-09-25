#!/usr/bin/env python3
"""Usage: p_id_audit.py <tree>
List every P-<NAME> identifier used in <tree>/docs/**/*.md that is not a row
key of F01.5 (docs/architecture/01_overview.md, the single P-ID registry per
docs/README.md section 2), and print the 06 section 11 parameter paragraph."""
import glob, re, sys, pathlib
tree = pathlib.Path(sys.argv[1])
f01 = (tree / 'docs/architecture/01_overview.md').read_text()
tbl = f01[f01.index('fig-01-params'):f01.index('**Profile mechanism**')]
defined = set()
for line in tbl.splitlines():
    if line.startswith('| P-'):
        defined.update(m.rstrip('-') for m in re.findall(r'P-[A-Z0-9-]+', line.split('|')[1]))
defined.discard('P-ID')
print(f'F01.5 P-IDs: {len(defined)}')
for p in sorted(glob.glob(str(tree / 'docs/**/*.md'), recursive=True)):
    ids = set(m.rstrip('-') for m in re.findall(r'(?<![A-Za-z0-9_])P-[A-Z][A-Z0-9-]+', open(p).read()))
    bad = sorted(i for i in ids if i not in defined)
    rel = pathlib.Path(p).relative_to(tree)
    print(f'{rel}: {len(ids)} P-IDs, not in F01.5: {bad if bad else "none"}')
s06 = (tree / 'docs/architecture/06_aecp_engine.md').read_text()
sec = s06[s06.index('## 11. Parameterization'):s06.index('## 12. Cross-references')]
print('--- 06 section 11 ---')
print(sec.rstrip())
