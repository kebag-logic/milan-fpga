#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Plant defects in a copy of the exact head and run the RV32 gate (Debug and Release).

usage: rv32_probe.py --tree <exported head tree> --work <dir>

Each plant must make scripts/baremetal.py fail through the QEMU exit code of the
generated-entity freshness check (entity_check_dafresh); the control must pass.
"""
import argparse
import json
import re
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

PLANTS = [
    ('control', None, None, None),
    ('rv-generated-window', 'examples/entities/talker/entity_config.c',
     '.da_fresh_ms = 15000u,', '.da_fresh_ms = 15001u,'),
    ('rv-answer-not-recorded', 'src/acmp.c', '\t\ts->answered = true;\n', ''),
    ('rv-gate-always-closed', 'src/acmp.c',
     'return st.dest_mac_valid && (s->answered || s->listener_registered);', 'return false;'),
    ('rv-window-zero', 'src/acmp.c',
     '(uint32_t)(now(a) - s->answered_at) >= a->cfg.da_fresh_ms', '(uint32_t)(now(a) - s->answered_at) >= a->cfg.da_fresh_ms / 65536u'),
]


def run(tree, work, plant):
    name, path, old, new = plant
    out = work / name
    if out.exists():
        shutil.rmtree(out)
    copy = out / 'tree'
    shutil.copytree(tree, copy)
    if path:
        text = (copy / path).read_text()
        assert text.count(old) == 1, name
        (copy / path).write_text(text.replace(old, new))
    log = out / 'baremetal.log'
    with open(log, 'w') as f:
        rc = subprocess.run(['python3', str(copy / 'scripts/baremetal.py'), '--work', str(out / 'rv32'), '--jobs', '4'],
                            cwd=copy, stdout=f, stderr=subprocess.STDOUT).returncode
    body = log.read_text()
    qemu = re.findall(r'command failed: (qemu-system-riscv32[^\n]*)', body)
    return {'plant': name, 'baremetal_rc': rc, 'qemu_failed': bool(qemu),
            'caught': rc != 0 if path else None, 'passes': rc == 0 if not path else None,
            'last_line': body.strip().splitlines()[-1] if body.strip() else ''}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--tree', type=Path, required=True)
    p.add_argument('--work', type=Path, required=True)
    a = p.parse_args()
    a.work.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(lambda pl: run(a.tree.resolve(), a.work.resolve(), pl), PLANTS))
    (a.work / 'rv32-probe.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=1))


if __name__ == '__main__':
    main()
