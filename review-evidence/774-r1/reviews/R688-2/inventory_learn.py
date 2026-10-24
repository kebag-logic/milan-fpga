#!/usr/bin/env python3
"""List every command-table entry a tree's own CI walk needs beyond its committed table, so the entries a change
adds can be told from its base's drift by comparing two trees' lists.

usage: CI_IMAGE_SHFMT=<pinned shfmt> python3 inventory_learn.py <root> <makefile> [<makefile> ...]
Runs the tree's own scripts/ci_command_table.py Audit (built as scripts/ci_tool_inventory.py builds it) over
each Makefile, all targets, with the table held in memory. Each refusal of these three kinds is answered in
memory and recorded, and the walk continues:
  changed declared script S        -> S re-pinned to its bytes
  undeclared executing ... S       -> S declared "reviewed non-installing"
  unclassified command NAME/ARGV   -> the exact normalized argv (runtime slots as "<runtime>") added as a pattern
Any other refusal is printed as the stop reason. Nothing is written to the tree. Each learned entry is printed as
one JSON line, sorted, so two runs diff line by line.
"""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
makefiles = sys.argv[2:]
sys.path.insert(0, str(root / 'scripts'))
import ci_command_table as cct  # noqa: E402  the tree's own walker
import ci_tool_inventory  # noqa: E402

learned = set()
table = json.loads((root / cct.TABLE).read_text())


class Learn(cct.Audit):
    def command(self, words, where, directory=None):
        for _ in range(4):
            try:
                return super().command(words, where, directory)
            except cct.Refusal as exc:
                if not str(exc).startswith('unclassified command'):
                    raise
                name = words[0]
                key = name if name == '.' else Path(name).name
                row = self.table['commands'].setdefault(
                    key, {'class': 'non-installing', 'executables': [key], 'patterns': []})
                exe = cct.normalize(name, self.root)
                if exe not in row.setdefault('executables', [key]):
                    row['executables'].append(exe)
                    learned.add(json.dumps({'command': key, 'executable': exe}))
                if not row.get('handler'):
                    pattern = ['<runtime>' if isinstance(w, cct.Runtime) else cct.normalize(w, self.root)
                               for w in words[1:]]
                    row.setdefault('patterns', []).append(pattern)
                    learned.add(json.dumps({'command': key, 'pattern': pattern,
                                            'at': re.sub(r':\d+(:\d+)?$', '', where)}))
        raise cct.Refusal(f'learning did not converge for {words[:1]} at {where}')


for makefile in makefiles:
    for attempt in range(100):
        audit = Learn(root, {})
        audit.table = table
        audit.install_reader = ci_tool_inventory.shell_installs
        try:
            audit.makefile(root / makefile)
            print(f'walked {makefile}: no refusal left ({attempt} script answers)', file=sys.stderr)
            break
        except cct.Refusal as exc:
            text = str(exc)
        changed = re.search(r"changed declared script '([^']+)'", text)
        undeclared = re.search(r"undeclared executing or network script '([^']+)'", text)
        if not (changed or undeclared):
            print(f'stop in {makefile}: {text}', file=sys.stderr)
            sys.exit(2)
        rel = (changed or undeclared).group(1)
        digest = cct.sha256(root / rel)
        if changed:
            table['scripts'][rel]['sha256'] = digest
            learned.add(json.dumps({'script': rel, 'repin': digest}))
        else:
            table['scripts'][rel] = {'class': 'reviewed non-installing', 'reason': 'learned', 'sha256': digest}
            learned.add(json.dumps({'script': rel, 'declare': digest}))
for line in sorted(learned):
    print(line)
