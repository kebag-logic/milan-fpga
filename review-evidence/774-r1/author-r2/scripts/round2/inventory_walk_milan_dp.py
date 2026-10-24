#!/usr/bin/env python3
"""The CI command-table audit (scripts/ci_command_table.py Audit, as scripts/ci_tool_inventory.py builds it)
started at one suite's Makefile, so a change's own entries are reached even where the whole-tree walk stops
earlier on its base's drift.

usage: CI_IMAGE_SHFMT=<pinned shfmt> python3 inventory_walk_milan_dp.py <disposable-root> [makefile]
Default makefile: tb/verilator/milan_dp/Makefile. Each "changed declared script" refusal re-pins that script in
the copy's ci/image/command-table.json and each "undeclared executing or network script" refusal declares it
"reviewed non-installing" in the copy, as inventory_walk_far.py does; any other refusal ends the walk. Prints
every refusal in order. Never point it at a checkout you care about.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
makefile = sys.argv[2] if len(sys.argv) > 2 else 'tb/verilator/milan_dp/Makefile'
sys.path.insert(0, str(root / 'scripts'))
import ci_command_table  # noqa: E402  the copy's own walker
import ci_tool_inventory  # noqa: E402

table_path = root / 'ci/image/command-table.json'
REASON = 'Validation and source inspection: invokes existing tools or local fixtures; installs nothing.'

for step in range(200):
    audit = ci_command_table.Audit(root, {})
    audit.install_reader = ci_tool_inventory.shell_installs
    try:
        audit.makefile(root / makefile)
        print(f'step {step}: no refusal; walked {makefile}; {len(audit.inputs)} inputs, '
              f'{len(audit.residue)} residue entries')
        names = sorted(k for k in audit.inputs if 'milan_dp' in k)
        print('  milan_dp inputs: ' + ', '.join(names))
        break
    except ci_command_table.Refusal as exc:
        text = str(exc)
    print(f'step {step}: REFUSED: {text}', flush=True)
    changed = re.search(r"changed declared script '([^']+)'", text)
    undeclared = re.search(r"undeclared executing or network script '([^']+)'", text)
    if not (changed or undeclared):
        print('stop: refusal outside the walk')
        sys.exit(2)
    rel = (changed or undeclared).group(1)
    table = json.loads(table_path.read_text())
    new = hashlib.sha256((root / rel).read_bytes()).hexdigest()
    if changed:
        print(f'  re-pin {rel}: {table["scripts"][rel]["sha256"]} -> {new}')
        table['scripts'][rel]['sha256'] = new
    else:
        print(f'  declare {rel}: reviewed non-installing {new}')
        table['scripts'][rel] = {'class': 'reviewed non-installing', 'reason': REASON, 'sha256': new}
        table['scripts'] = dict(sorted(table['scripts'].items()))
    table_path.write_text(json.dumps(table, indent=2, ensure_ascii=False) + '\n')
