#!/usr/bin/env python3
"""count_plants.py LABEL=LOG...: count, in each complete firmware-gate log, the lines the gate itself prints for what
it ran, by kind, and print one row a log with the log's size and sha256 (so it can be matched to a published excerpt's
header). Kinds:
  suite arms      `[ok] arm ...` / `[FAIL] arm ...`  (ctrl_arms.report: a normal suite run, not a plant)
  control plants  `[ok] mutant ...` / `[ESCAPED] mutant ...`, and the campaign's own `mutants: N of M caught` line
  pin controls    `[ok] lwSRP pin, ...` (ctrl_mutants.lwsrp_pin_arms: a dependency-pin refusal, not a firmware plant)
  plants          every other `[ok] <name>:` / `[ESCAPED] <name>:` line (aecp_mutants and srp_mutants campaigns, one a
                  plant); split into campaigns where a name repeats, since each campaign walks its table in order
Nothing is inferred from file names or from any summary not printed by the gate."""
import hashlib
import re
import sys
from pathlib import Path

for arg in sys.argv[1:]:
    label, _, path = arg.partition('=')
    data = Path(path).read_bytes()
    text = data.decode(errors='replace').splitlines()
    arms = {'ok': 0, 'FAIL': 0}
    mut = {'ok': 0, 'ESCAPED': 0}
    pins = {'ok': 0, 'ESCAPED': 0}
    plants = {'ok': 0, 'ESCAPED': 0}
    totals = [ln for ln in text if ln.startswith('mutants: ')]
    inventory = [ln for ln in text if 'live invocations in exactly one shard' in ln]
    segs = [[]]
    for ln in text:
        m = re.match(r'\[(ok|FAIL|ESCAPED)\] (.*)', ln)
        if not m:
            continue
        verdict, rest = m.groups()
        if rest.startswith('arm '):
            arms[verdict if verdict in arms else 'FAIL'] += 1
        elif rest.startswith('mutant '):
            mut['ok' if verdict == 'ok' else 'ESCAPED'] += 1
        elif rest.startswith('lwSRP pin'):
            pins['ok' if verdict == 'ok' else 'ESCAPED'] += 1
        else:
            plants['ok' if verdict == 'ok' else 'ESCAPED'] += 1
            name = rest.split(':', 1)[0]
            if name in segs[-1]:
                segs.append([])
            segs[-1].append(name)
    campaigns = [len(s) for s in segs if s]
    print(f"{label}: {len(data):,} B sha256 {hashlib.sha256(data).hexdigest()}")
    print(f"  suite arms ok {arms['ok']} fail {arms['FAIL']}; control plants ok {mut['ok']} escaped {mut['ESCAPED']}"
          f"{' (' + totals[-1] + ')' if totals else ''}; plants ok {plants['ok']} escaped {plants['ESCAPED']}"
          f"{' in campaigns ' + str(campaigns) if len(campaigns) > 1 else ''}; pin controls ok {pins['ok']}"
          f" escaped {pins['ESCAPED']}")
    for ln in inventory:
        print(f"  inventory: {ln.strip()}")
