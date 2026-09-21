# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R218's round-two probe, ADAPTED to run against the revision-c evidence.

The original is review-evidence/503-round2/R218/probe_headers.py at commit
7d9da877 (sha256 d713e83d44aa09d2791a3ebb8f2d51d6d556c62b6caf42802f8247f67ff28ad9).
Every stimulus and variant is the reviewer's ("Reviewer-owned stimuli;
original published RTL, firmware and graders" in the original). Three
adaptations, and only these:

1. PATH CONSTANTS come from the environment: PROBE_OUT (a scratch directory,
   required) and EVIDENCE (the proposal-evidence directory, default this
   file's sibling).
2. THE ONE SEAM THAT MOVED: V18's `read_fault(0x50, 0, -1, 1);` now also
   occurs in H2 and H2b, so the anchor carries V18's comment line to stay
   unique; the replacement is the reviewer's.
3. The V1a slots the variants boot from come from a V1a seed run of this
   probe's own build (the reviewer took them from the full run's V1a), and
   the recorded result also carries the terminal's defaults mismatches for
   the two original-trigger runs (a record of output, not a stimulus).

It writes probes/results.json under PROBE_OUT/r218; r218_check.py grades it
against the behaviour the reviewer demanded.
"""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys

SCRATCH = Path(os.environ["PROBE_OUT"]) / 'r218'
PE = Path(os.environ.get("EVIDENCE", Path(__file__).resolve().parents[1] / "proposal-evidence"))
os.environ['D3_OUT'] = str(SCRATCH / 'probes')
os.environ['OOC_OUT'] = str(SCRATCH / 'ooc')
spec = importlib.util.spec_from_file_location('review_d3', PE / 'run.py')
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)
harness = SCRATCH / 'probe-harness'
if harness.exists():
    shutil.rmtree(harness)
shutil.copytree(PE / 'harness', harness)
p = harness / 'd3_cases.cpp'
t = p.read_text()
# ADAPTATION 2: V18's own comment line keeps the anchor unique
old = ("    // erased record; the port's cause makes it a transport failure (cause 2)\n"
       '    read_fault(0x50, 0, -1, 1);\n    restore_under_fault();')
new = ("    // erased record; the port's cause makes it a transport failure (cause 2)\n"
       '''    if (variant == "repeat") read_fault(0x50, 0, -1);
    else if (variant == "swap") {
      read_fault(0x51, 0, -1, 0);
      read_fault(0x50, 0, -1, 1);
    } else if (variant == "pass0") read_fault(0x50, 0, -1, 0);
    else read_fault(0x50, 0, -1, 1);
    restore_under_fault();''')
assert t.count(old) == 1
t = t.replace(old, new)
# Exactly the first external review's fault: after ANY earlier application.
old = '    read_fault(0x80, 8 + 16, -1, 1);'
new = '    read_fault(0x80, 8 + 16, -1);'
assert t.count(old) == 1
t = t.replace(old, new)
# Reuse W12's logging/recovery, but arm the delay at the original trigger.
old = '    hold_read(0x30, 1, 1, 3100000);'
assert t.count(old) == 1
t = t.replace(old, '    // The bridge arms the original after-any-application delay.\n')
p.write_text(t)
p = harness / 'd3_bridge.cpp'
t = p.read_text()
old = '  if (addr < kBase) return nullptr;'
new = '''  if (addr < kBase) return nullptr;
  if (std::getenv("R218_ORIGINAL_F1") && dut->d3_rs_applied_o == 0) return nullptr;'''
assert t.count(old) == 1
t = t.replace(old, new)
old = '    rd = Rd{true, 2, dut->mem_req_addr_o};'
new = '''    static bool r218_delayed = false;
    if (std::getenv("R218_ORIGINAL_F2") && !r218_delayed && dut->d3_rs_applied_o != 0) {
      rdhold = RdHold{};
      rdhold.armed = true;
      rdhold.rid = -1;
      rdhold.pass = -1;
      rdhold.nth = 1;
      rdhold.hold = 3100000;
      r218_delayed = true;
    }
    rd = Rd{true, 2, dut->mem_req_addr_o};'''
assert t.count(old) == 1
p.write_text(t.replace(old, new))
m.HARNESS = harness
m.STUBS = harness / 'stubs'
s = m.prep_shape('1x1')
b = m.do_build(m.Build('reviewer-headers', '1x1'), s, 8)
# ADAPTATION 3: the V1a slots from a seed run of this build
seed = m.run_case(b, s, m.V1A)
assert seed.rc == 0 and seed.done
source = seed.out
slots = source / 'cut-slotA.bin', source / 'cut-slotB.bin'
results = []
for variant in ['pass0', 'pass1', 'repeat', 'swap']:
    r = m.run_case(b, s, 'V18_header_error_pass1', variant, slots)
    g = m.Grade(r, s)
    extra = {'cut_slots': g.slots(*slots)}
    g = m.grade_run(r, s, extra)
    result = {'variant': variant, 'rc': r.rc, 'done': r.done,
              'terminal': r.obs.get('terminal'), 'boot': g.boot(), 'checks': g.checks,
              'mismatches_saved': g.mismatches(r.snaps['terminal'], {k:v for k,v in extra['cut_slots'].items() if k in g.d3_rids()}),
              'mismatches_defaults': g.mismatches(r.snaps['terminal'], {})}
    results.append(result)
    print(json.dumps(result), flush=True)
for env,case in [('R218_ORIGINAL_F1', 'V11b_torn_in_pass1_rolls_back'), ('R218_ORIGINAL_F2', 'W12_r218_read_late_after_apply')]:
    os.environ[env] = '1'
    inputs = slots
    if env.endswith('F1'):
        inputs,_ = m.crafted_for(s, 'V11_torn_read_restores_nothing')
    r = m.run_case(b, s, case, 'original-trigger', inputs)
    g = m.grade_run(r, s, {'cut_slots': m.Grade(r,s).slots(*inputs)})
    result = {'variant': env, 'rc': r.rc, 'done': r.done, 'terminal': r.obs.get('terminal'), 'boot': g.boot(), 'checks': g.checks,
              'mismatches_defaults': g.mismatches(r.snaps['terminal'], {})}
    results.append(result)
    print(json.dumps(result), flush=True)
    del os.environ[env]
(SCRATCH / 'probes/results.json').write_text(json.dumps(results, indent=2) + '\n')
