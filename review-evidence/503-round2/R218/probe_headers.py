"""Reviewer-owned stimuli; original published RTL, firmware and graders."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys

SCRATCH = Path(__file__).resolve().parent
PE = SCRATCH / 'evidence/design-evidence/500-materialization/proposal-evidence'
os.environ['D3_OUT'] = str(SCRATCH / 'probes')
os.environ['OOC_OUT'] = str(SCRATCH / 'ooc')
os.environ['TMPDIR'] = str(SCRATCH / 'tmp')
spec = importlib.util.spec_from_file_location('review_d3', PE / 'run.py')
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)
harness = SCRATCH / 'probe-harness'
shutil.copytree(PE / 'harness', harness)
p = harness / 'd3_cases.cpp'
t = p.read_text()
old = '    read_fault(0x50, 0, -1, 1);\n    restore_under_fault();'
new = '''    if (variant == "repeat") read_fault(0x50, 0, -1);
    else if (variant == "swap") {
      read_fault(0x51, 0, -1, 0);
      read_fault(0x50, 0, -1, 1);
    } else if (variant == "pass0") read_fault(0x50, 0, -1, 0);
    else read_fault(0x50, 0, -1, 1);
    restore_under_fault();'''
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
source = SCRATCH / 'd3/runs/base-1x1/V1a_set_everything'
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
    result = {'variant': env, 'rc': r.rc, 'done': r.done, 'terminal': r.obs.get('terminal'), 'boot': g.boot(), 'checks': g.checks}
    results.append(result)
    print(json.dumps(result), flush=True)
    del os.environ[env]
(SCRATCH / 'probes/results.json').write_text(json.dumps(results, indent=2) + '\n')
