"""Run complete declared gate tables in foreground partitions with retained receipts."""
import argparse
import ast
import json
import os
from pathlib import Path
import sys
import time

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--root', type=Path, required=True)
p.add_argument('--scratch', type=Path, required=True)
p.add_argument('--family', choices=('ctrl', 'srp', 'srp1', 'builder'), required=True)
p.add_argument('--part', type=int, required=True)
p.add_argument('--parts', type=int, required=True)
a = p.parse_args()
assert 0 <= a.part < a.parts
a.root = a.root.resolve()
a.scratch = a.scratch.resolve()
os.chdir(a.root)
out = a.scratch / f'{a.family}-partition-{a.part}-of-{a.parts}'
out.mkdir(parents=True, exist_ok=True)
start = time.monotonic()
names = []
failed = False
if a.family in ('ctrl', 'srp', 'srp1'):
    sys.path.insert(0, str(a.root / 'sw/firmware/ctrl/test'))
    import ctrl_mutants
    import srp_mutants
    if a.family == 'ctrl':
        names = [m.name for m in ctrl_mutants.MUTANTS[a.part::a.parts]]
        failed = ctrl_mutants.campaign(out, a.scratch / 'firmware-bank-final/reuse',
                                      4, shard=[a.part, a.parts])
    else:
        table = srp_mutants.DEFECTS
        if a.family == 'srp1':
            table = tuple(d for d in table if d.name.startswith((
                'four-way-', 'binding-', 'feedback-', 'r10-', 'p11-', 'srp-bound-',
                'srp-term-', 'srp-poll-extra', 'srp-send-extra')))
        srp_mutants.DEFECTS = table[a.part::a.parts]
        names = [d.name for d in srp_mutants.DEFECTS]
        failed = srp_mutants.campaign(out, a.root / 'third_party/lwSRP', 4,
                                     1 if a.family == 'srp1' else 2)
else:
    sys.path.insert(0, str(a.root / 'sw/builder'))
    sys.argv = [sys.argv[0], '--require-rv32']
    import test_builder as bank
    import test_declarations
    import test_clock_contract
    source = ast.parse((a.root / 'sw/builder/test_builder.py').read_text())
    loop = next(n for n in ast.walk(source) if isinstance(n, ast.For)
                and isinstance(n.target, ast.Name) and n.target.id == 'fn')
    table = [n.id for n in loop.iter.elts if n.id != 'test_baremetal_profile_contract']
    names = table[a.part::a.parts]
    for name in names:
        fn = next(getattr(module, name) for module in
                  (bank, test_declarations, test_clock_contract) if hasattr(module, name))
        print(name + ':', flush=True)
        fn()
    print('Explicit non-executed arms:', bank.SKIPPED, flush=True)
receipt = {'family': a.family, 'part': a.part, 'parts': a.parts, 'names': names,
           'rc': int(failed), 'seconds': time.monotonic() - start}
(out / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt), flush=True)
raise SystemExit(failed)
