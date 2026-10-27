"""Compare the README's mutant table (the two-column table after 'replaces each rule in turn') with
the self-test's 'MUTANT caught: <name>: <check>' lines. usage: mutant_table.py README SELFTEST_LOG"""
import re
import sys
text = open(sys.argv[1]).read()
section = text[text.index('replaces each rule in turn'):]
section = section[:section.index('\n\n', section.index('|---'))]
rows = {}
for line in section.splitlines():
    m = re.match(r'^\| (.+?) \| (.+?) \|$', line)
    if m and not m.group(1).startswith('---') and m.group(1) != 'Mutant':
        rows[m.group(1)] = m.group(2)
caught = [l[len('MUTANT caught: '):] for l in open(sys.argv[2]).read().splitlines() if l.startswith('MUTANT caught: ')]
matched, bad = 0, []
for line in caught:
    name = next((n for n in sorted(rows, key=len, reverse=True) if line.startswith(n + ': ')), None)
    if name is None:
        bad.append(('no README row', line[:100]))
    elif not line[len(name) + 2:].startswith(rows[name]):
        bad.append(('check differs', name, rows[name], line[len(name) + 2:][:100]))
    else:
        matched += 1
print(f'README rows {len(rows)}, self-test mutants caught {len(caught)}, matched {matched}')
for b in bad:
    print('DIFF', b)
