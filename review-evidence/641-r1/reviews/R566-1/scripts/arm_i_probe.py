#!/usr/bin/env python3
"""Reviewer probe of #641 items 1 and 2 against one tree and the make first on PATH.

For each variant (head; MAKEFLAGS= guard removed from one consumer; inventory
reverted to the PR base; a planted $(error) after a rule), applies the edit in
TREE, asks the arm-I inventory about tb/verilator/milan_dp_render/Makefile and
tb/verilator/pp_shadow/Makefile, prints one JSON row per (variant, consumer),
and restores the tracked bytes with git checkout.

usage: arm_i_probe.py TREE BASE_REV
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

CONSUMERS = ('tb/verilator/milan_dp_render/Makefile', 'tb/verilator/pp_shadow/Makefile')


def run_inventory(tree: Path) -> list[dict]:
    code = r'''
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, "scripts")
import shape_consumer_inventory as inv
tracked = set(subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True).stdout.split())
rows = []
for name in %r:
    p = Path(name)
    ok, prereqs = inv.shape_prereqs_from_database(p.parent, p.name)
    dangling = inv.dangling_consumers(name, p.read_text(), tracked)
    rows.append(dict(consumer=name, database_ok=ok, frozen_shape_prereqs=prereqs, dangling=[str(d) for d in dangling]))
print(json.dumps(rows))
''' % (CONSUMERS,)
    out = subprocess.run([sys.executable, '-c', code], cwd=tree, capture_output=True, text=True)
    if out.returncode:
        return [dict(error=out.stderr[-800:])]
    return json.loads(out.stdout.strip().splitlines()[-1])


def main() -> int:
    tree, base = Path(sys.argv[1]).resolve(), sys.argv[2]
    make = subprocess.run(['make', '--version'], capture_output=True, text=True).stdout.splitlines()[0]

    def unguard(path: str):
        def edit():
            f = tree / path
            f.write_text(f.read_text().replace('MAKEFLAGS= $(MAKE) -s --no-print-directory', '$(MAKE) -s'))
        return edit

    def base_inventory():
        text = subprocess.run(['git', 'show', f'{base}:scripts/shape_consumer_inventory.py'], cwd=tree,
                              capture_output=True, text=True, check=True).stdout
        (tree / 'scripts/shape_consumer_inventory.py').write_text(text)

    def planted_error(path: str):
        def edit():
            f = tree / path
            f.write_text('fixture: missing-generated-input\n$(error reviewer planted stop)\n' + f.read_text())
        return edit

    variants = [
        ('head', []),
        ('render-unguarded', [unguard(CONSUMERS[0])]),
        ('shadow-unguarded', [unguard(CONSUMERS[1])]),
        ('render-unguarded+base-inventory', [unguard(CONSUMERS[0]), base_inventory]),
        ('shadow-unguarded+base-inventory', [unguard(CONSUMERS[1]), base_inventory]),
        ('render-planted-error', [planted_error(CONSUMERS[0])]),
        ('render-planted-error+base-inventory', [planted_error(CONSUMERS[0]), base_inventory]),
    ]
    for label, edits in variants:
        try:
            for edit in edits:
                edit()
            for row in run_inventory(tree):
                print(json.dumps(dict(make=make, variant=label, **row)), flush=True)
        finally:
            subprocess.run(['git', 'checkout', '--', 'scripts/shape_consumer_inventory.py', *CONSUMERS],
                           cwd=tree, check=True)
    dirty = subprocess.run(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=tree,
                           capture_output=True, text=True).stdout
    print(json.dumps(dict(make=make, restored_clean=not dirty.strip())))
    return 0


if __name__ == '__main__':
    sys.exit(main())
