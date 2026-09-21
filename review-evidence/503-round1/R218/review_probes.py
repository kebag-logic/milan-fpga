"""Reviewer-only probes. No tracked source is edited."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys

ROOT = Path('/data/milan/reviews/r218-503-evidence')
SCRATCH = Path('/data/milan/reviews/r218-503-scratch')
PE = ROOT / 'design-evidence/500-materialization/proposal-evidence'
os.environ['D3_OUT'] = str(SCRATCH / 'probes')
os.environ['OOC_OUT'] = str(SCRATCH / 'ooc')
os.environ['TMPDIR'] = str(SCRATCH / 'tmp')
spec = importlib.util.spec_from_file_location('d3_run', PE / 'run.py')
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)
mode = sys.argv[1]
m.HERE = SCRATCH / ('report-' + mode)
m.HERE.mkdir(exist_ok=True)
s = m.prep_shape('1x1')

if mode == 'surviving-killer':
    # The base binary is a deliberately ineffective/no-op version of M01.
    # Keep the real K2 stimulus, real observations, and original named grader.
    b = m.Build('mut-M01_taint_ignored', '1x1')
    b.binary = SCRATCH / 'd3/build/base-1x1/obj/d3sim'
    r = m.run_case(b, s, 'K2_change_during_record_write')
    g = m.grade_run(r, s, {})
    assert g.checks['no_durable_claim_over_unsaved'][0] is True
    m.report({b.name: [(r, g)]})
    # Deliberately follow run.py main(): report's failure count is discarded.
    raise SystemExit(0)

harness = SCRATCH / ('harness-' + mode)
shutil.copytree(PE / 'harness', harness)
bridge = harness / 'd3_bridge.cpp'
text = bridge.read_text()
if mode == 'second-pass':
    old = '  if (addr < kBase) return nullptr;'
    new = ('  // Arm the existing V11 fault only after pass 1 has applied a record.\n'
           '  if (addr < kBase || dut->d3_rs_applied_o == 0) return nullptr;')
elif mode == 'timeout':
    old = '  if (rtake) rd = Rd{true, 2, dut->mem_req_addr_o};'
    new = '''  if (rtake) {
    static bool delayed = false;
    const bool delay_now = !delayed && dut->d3_rs_applied_o != 0;
    rd = Rd{true, delay_now ? 3100000 : 2, dut->mem_req_addr_o};
    delayed = delayed || delay_now;
  }'''
else:
    raise SystemExit('unknown mode')
assert text.count(old) == 1
bridge.write_text(text.replace(old, new))
(m.HERE / 'injection.txt').write_text(old + '\nBECOMES\n' + new + '\n')
m.HARNESS = harness
m.STUBS = harness / 'stubs'
b = m.do_build(m.Build('probe-' + mode, '1x1'), s, 8)
if mode == 'second-pass':
    case = 'V11_torn_read_restores_nothing'
    slots, over = m.crafted_for(s, case)
    extra = {'crafted': over}
else:
    case = 'V1b_restore_everything'
    src = SCRATCH / 'd3/runs/base-1x1/V1a_set_everything'
    slots = (src / 'cut-slotA.bin', src / 'cut-slotB.bin')
    extra = {}
r = m.run_case(b, s, case, slots=slots)
if mode == 'timeout':
    extra['cut_slots'] = m.Grade(r, s).slots(*slots)
g = m.grade_run(r, s, extra)
result = {'checks': g.checks, 'boot': g.boot(), 'firmware': r.fw,
          'restored': r.obs.get('restored'), 'case_exit': r.rc}
(m.HERE / 'result.json').write_text(json.dumps(result, indent=2))
for name, (ok, detail) in g.checks.items():
    print('PASS' if ok else 'FAIL', name, '--', detail)
print('BOOT', g.boot())
print('FIRMWARE', r.fw)
