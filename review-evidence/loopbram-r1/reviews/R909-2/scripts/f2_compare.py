#!/usr/bin/env python3
"""Compare canonical disabled release-top netlists base vs head, raw-canonical
and with the one path-derived identifier normalized: LiteX names the generated
CPU wrapper VexiiRiscvLitex_<md5 of every SoC argparse value>, and those values
include the export's absolute output and firmware paths. Also report every
differing line class.

usage: f2_compare.py <elab-root> [<author-canonical-1x1.v>]
"""
import difflib
import hashlib
import json
import re
import sys
from pathlib import Path

CPU = re.compile(r'VexiiRiscvLitex_[0-9a-f]{32}')
root = Path(sys.argv[1])
author = Path(sys.argv[2]) if len(sys.argv) > 2 else None
out = []
for name in ('endstation_ax7101_1x1_tdm8', 'endstation_ax7101_8x8'):
    text = {s: (root / s / name / 'canonical.v').read_text() for s in ('base', 'head')}
    norm = {s: CPU.sub('VexiiRiscvLitex_CPU', t) for s, t in text.items()}
    diff = [l for l in difflib.unified_diff(text['base'].splitlines(), text['head'].splitlines(), lineterm='', n=0)
            if l[:1] in '+-' and not l.startswith(('+++', '---'))]
    other = [l for l in diff if not CPU.search(l)]
    entry = dict(shape=name,
                 canonical_sha256={s: hashlib.sha256(t.encode()).hexdigest() for s, t in text.items()},
                 cpu_normalized_sha256={s: hashlib.sha256(t.encode()).hexdigest() for s, t in norm.items()},
                 cpu_names={s: sorted(set(CPU.findall(t))) for s, t in text.items()},
                 differing_lines=len(diff), differing_lines_without_cpu_name=len(other),
                 identical_after_cpu_name=norm['base'] == norm['head'])
    if author is not None and name == 'endstation_ax7101_1x1_tdm8' and author.is_file():
        a = author.read_text()
        entry['author_canonical_sha256'] = hashlib.sha256(a.encode()).hexdigest()
        entry['author_cpu_normalized_equals_head'] = CPU.sub('VexiiRiscvLitex_CPU', a) == norm['head']
    out.append(entry)
print(json.dumps(out, indent=2))
raise SystemExit(0 if all(e['identical_after_cpu_name'] and e['differing_lines_without_cpu_name'] == 0
                          for e in out) else 1)
