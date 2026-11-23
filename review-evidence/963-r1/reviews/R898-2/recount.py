#!/usr/bin/env python3
"""recount.py LABEL=LOG...: independently classify the verdict lines a firmware-gate log prints, by the printer that
emits them in the gate's source at the reviewed head:
  ctrl_arms.report        "[ok] arm ..." / "[FAIL] arm ..."            -> suite arms (shard 0; not plants)
  ctrl_mutants.campaign   "[ok] mutant ..." / "[ESCAPED] mutant ..."   -> control plants (shard 1), and its
                          own "mutants: N of M caught" summary line
  ctrl_mutants pin arms   "[ok] lwSRP pin, ..."                        -> dependency-pin controls (not plants)
  aecp/srp campaign()     "[ok] NAME: TESTS" / "[ESCAPED] NAME: TESTS" -> plants (shards 2 and 3)
plus the shard inventory line. Prints size, sha256 and counts for each log."""
import hashlib
import re
import sys

for arg in sys.argv[1:]:
    label, _, path = arg.partition('=')
    raw = open(path, 'rb').read()
    lines = raw.decode(errors='replace').splitlines()
    c = {k: 0 for k in ('arm-ok', 'arm-fail', 'ctl-ok', 'ctl-esc', 'pin-ok', 'pin-esc', 'plant-ok', 'plant-esc', 'other')}
    for ln in lines:
        m = re.match(r'\[(ok|FAIL|ESCAPED)\] (.*)$', ln)
        if not m:
            continue
        v, rest = m.groups()
        good = v == 'ok'
        if rest.startswith('arm '):
            c['arm-ok' if good else 'arm-fail'] += 1
        elif rest.startswith('mutant '):
            c['ctl-ok' if good else 'ctl-esc'] += 1
        elif rest.startswith('lwSRP pin'):
            c['pin-ok' if good else 'pin-esc'] += 1
        elif re.match(r'[\w.+-]+: ', rest):
            c['plant-ok' if good else 'plant-esc'] += 1
        else:
            c['other'] += 1
    summ = [ln for ln in lines if ln.startswith('mutants: ')]
    inv = [ln.strip() for ln in lines if 'live invocations in exactly one shard' in ln]
    print(f"{label}: {len(raw)} B sha256 {hashlib.sha256(raw).hexdigest()}")
    print("  " + " ".join(f"{k}={v}" for k, v in c.items()) + (f" | {summ[-1]}" if summ else ""))
    for ln in inv:
        print(f"  inventory: {ln}")
